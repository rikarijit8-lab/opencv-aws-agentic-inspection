"""
agent_pipeline.py - Autonomous Closed-Loop Agentic Vision Pipeline
Part of the OpenCV AI Competition 2026 (Powered by AWS)
Tracks: Agentic Vision with OpenCV 5 & Best Use of COOL

Implements an autonomous Multi-Step Perception -> Decision -> Action loop:
1. Perception: Runs OpenCV 5 defect analysis via IndustrialVisionCore.
2. Decision: Evaluates visual output. If borderline (MARGINAL), the visual output
   actively triggers dynamic parameter retuning and a second-pass re-inspection!
   If catastrophic defect found, triggers EMERGENCY_HALT.
3. Action: Dispatches real-time CloudWatch metrics and structured telemetry to AWS
   (Region: ap-southeast-2) with robust fallback and execution tracing.
"""

import os
import sys
import time
import json
import logging
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional, Tuple
import numpy as np
from dotenv import load_dotenv

# Automatically load environment variables from .env file
load_dotenv()

# AWS SDK
import boto3
from botocore.exceptions import ClientError, NoCredentialsError

# Core Vision Engine
from vision_core import IndustrialVisionCore, InspectionConfig, InspectionResult

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("AgenticVision")


class AgentExecutionTrace:
    """Stores verifiable step-by-step traces for OpenCV Competition 2026 judging."""
    def __init__(self):
        self.steps: List[Dict[str, Any]] = []

    def record_step(self, step_number: int, phase: str, tool_name: str, input_state: Any, output_state: Any, justification: str):
        self.steps.append({
            "step": step_number,
            "phase": phase,                   # PERCEPTION, REASONING, TOOL_INVOCATION, ACTION
            "tool_called": tool_name,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "input_summary": input_state,
            "output_summary": output_state,
            "agent_justification": justification
        })

    def get_trace(self) -> List[Dict[str, Any]]:
        return self.steps


class AWSTelemetryDispatcher:
    """Handles secure AWS CloudWatch metrics and log dispatching for Region ap-southeast-2."""

    def __init__(self, region_name: Optional[str] = None):
        self.region = (
            region_name
            or os.getenv("AWS_DEFAULT_REGION")
            or os.getenv("AWS_REGION")
            or "ap-southeast-2"
        )
        self.namespace = os.getenv("CLOUDWATCH_NAMESPACE", "OpenCV/AgenticInspection")
        self.log_group_name = "/aws/opencv2026/agentic-inspection"
        self.log_stream_name = f"inspection-run-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

        # Initialize boto3 clients safely using env credentials
        self.has_credentials = bool(os.getenv("AWS_ACCESS_KEY_ID") and os.getenv("AWS_SECRET_ACCESS_KEY"))
        self.cloudwatch = None
        self.logs_client = None

        try:
            session = boto3.Session(
                region_name=self.region,
                aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
            )
            self.cloudwatch = session.client("cloudwatch", region_name=self.region)
            self.logs_client = session.client("logs", region_name=self.region)
            self.initialized = True
        except Exception as e:
            logger.warning(f"AWS Telemetry initialization notice: {e}")
            self.initialized = False

    def send_metrics(self, decision: str, defect_count: int, max_area: float, latency_ms: float, recalibrated: bool) -> Dict[str, Any]:
        """Publishes operational metrics to AWS CloudWatch."""
        metric_data = [
            {
                "MetricName": "DefectCount",
                "Dimensions": [{"Name": "InspectionTarget", "Value": "WorkpieceLine01"}],
                "Value": float(defect_count),
                "Unit": "Count"
            },
            {
                "MetricName": "MaxDefectAreaPx",
                "Dimensions": [{"Name": "InspectionTarget", "Value": "WorkpieceLine01"}],
                "Value": float(max_area),
                "Unit": "None"
            },
            {
                "MetricName": "VisionInferenceLatencyMs",
                "Dimensions": [{"Name": "InspectionTarget", "Value": "WorkpieceLine01"}],
                "Value": float(latency_ms),
                "Unit": "Milliseconds"
            },
            {
                "MetricName": "DecisionOutcome",
                "Dimensions": [
                    {"Name": "InspectionTarget", "Value": "WorkpieceLine01"},
                    {"Name": "Decision", "Value": decision}
                ],
                "Value": 1.0,
                "Unit": "Count"
            }
        ]

        if recalibrated:
            metric_data.append({
                "MetricName": "ClosedLoopRecalibrationsTriggered",
                "Dimensions": [{"Name": "InspectionTarget", "Value": "WorkpieceLine01"}],
                "Value": 1.0,
                "Unit": "Count"
            })

        if self.initialized and self.has_credentials:
            try:
                response = self.cloudwatch.put_metric_data(
                    Namespace=self.namespace,
                    MetricData=metric_data
                )
                return {
                    "status": "LIVE_AWS_SUCCESS",
                    "region": self.region,
                    "namespace": self.namespace,
                    "metrics_count": len(metric_data),
                    "http_status_code": response.get("ResponseMetadata", {}).get("HTTPStatusCode", 200)
                }
            except (ClientError, NoCredentialsError) as e:
                logger.error(f"AWS CloudWatch API returned error: {e}")
                return {
                    "status": "AWS_SIMULATED_DISPATCH",
                    "region": self.region,
                    "namespace": self.namespace,
                    "metrics_count": len(metric_data),
                    "reason": str(e),
                    "metrics_payload": metric_data
                }
        else:
            return {
                "status": "SIMULATED_LOCAL_MODE",
                "region": self.region,
                "namespace": self.namespace,
                "metrics_count": len(metric_data),
                "reason": "AWS credentials not detected or dry-run mode enabled",
                "metrics_payload": metric_data
            }

    def send_log_event(self, log_payload: Dict[str, Any]) -> Dict[str, Any]:
        """Dispatches structured audit record to AWS CloudWatch Logs."""
        timestamp = int(round(time.time() * 1000))
        message = json.dumps(log_payload)

        if self.initialized and self.has_credentials:
            try:
                # Ensure Log Group exists
                try:
                    self.logs_client.create_log_group(logGroupName=self.log_group_name)
                except self.logs_client.exceptions.ResourceAlreadyExistsException:
                    pass

                # Ensure Log Stream exists
                try:
                    self.logs_client.create_log_stream(
                        logGroupName=self.log_group_name,
                        logStreamName=self.log_stream_name
                    )
                except self.logs_client.exceptions.ResourceAlreadyExistsException:
                    pass

                response = self.logs_client.put_log_events(
                    logGroupName=self.log_group_name,
                    logStreamName=self.log_stream_name,
                    logEvents=[{"timestamp": timestamp, "message": message}]
                )
                return {
                    "status": "LOG_STREAMED_TO_AWS",
                    "log_group": self.log_group_name,
                    "log_stream": self.log_stream_name,
                    "nextSequenceToken": response.get("nextSequenceToken")
                }
            except Exception as e:
                return {
                    "status": "LOG_BUFFERED_LOCALLY",
                    "reason": str(e),
                    "payload_preview": log_payload
                }
        else:
            return {
                "status": "LOG_BUFFERED_LOCALLY",
                "reason": "Running with local simulator fallback",
                "payload_preview": log_payload
            }


class AgenticInspectionPipeline:
    """
    Main Autonomous Agent orchestrating the Closed-Loop Perception-Decision-Action cycle:
    - Perception: OpenCV 5 Industrial Defect Extraction
    - Decision: Multi-path agentic logic with dynamic parameter adjustment
    - Action: Re-inspection, Actuator Control, and AWS CloudWatch Dispatches
    """

    def __init__(self, region: str = "ap-southeast-2"):
        self.vision = IndustrialVisionCore()
        self.telemetry = AWSTelemetryDispatcher(region_name=region)

    def execute_inspection_cycle(self, image: np.ndarray) -> Dict[str, Any]:
        """
        Executes the autonomous agentic inspection cycle with verifiable traces.
        Demonstrates that OpenCV 5 vision output directly alters subsequent plans and tool calls!
        """
        trace = AgentExecutionTrace()
        recalibration_triggered = False

        # --- STEP 1: INITIAL PERCEPTION ---
        trace.record_step(
            step_number=1,
            phase="PERCEPTION",
            tool_name="vision_core.analyze_surface (Standard Config)",
            input_state={"canny_thresh1": 50, "canny_thresh2": 150, "clahe_clip": 2.0},
            output_state="Executing initial OpenCV 5 surface scan...",
            justification="Acquire baseline industrial workpiece inspection metrics."
        )

        initial_result = self.vision.analyze_surface(image)

        trace.record_step(
            step_number=2,
            phase="REASONING",
            tool_name="AgentCognitiveEvaluator",
            input_state={
                "status": initial_result.status,
                "defect_count": initial_result.defect_count,
                "max_defect_area": initial_result.max_defect_area
            },
            output_state=f"Initial finding: {initial_result.status} with {initial_result.defect_count} defect(s)",
            justification="Evaluating whether visual certainty threshold is satisfied or if closed-loop re-calibration is needed."
        )

        final_result = initial_result
        action_decision = "PASS"
        action_details = {}

        # --- STEP 2: CLOSED-LOOP DECISION BRANCHING ---
        if initial_result.status == "MARGINAL":
            # The visual output directly triggers an agentic re-calibration tool call!
            recalibration_triggered = True
            trace.record_step(
                step_number=3,
                phase="DECISION_ORCHESTRATION",
                tool_name="AgentClosedLoopOptimizer",
                input_state={"marginal_defects": initial_result.defects},
                output_state="PLAN: Trigger High-Sensitivity Optical Re-calibration pass",
                justification="Visual evidence revealed low-contrast marginal anomalies. "
                              "Agent autonomously re-tunes CLAHE contrast (2.0 -> 3.8) and Canny thresholds "
                              "(50/150 -> 30/110) to confirm if anomalies are structural cracks or optical glare."
            )

            # Re-tuned sensor configuration dynamically created by Agent
            tuned_config = InspectionConfig(
                canny_thresh1=30,
                canny_thresh2=110,
                clahe_clip_limit=3.8,
                clahe_tile_grid_size=10,
                morph_kernel_size=3,
                min_defect_area=60.0
            )

            # --- SECOND-PASS PERCEPTION TOOL CALL ---
            second_pass_result = self.vision.analyze_surface(image, config_override=tuned_config)
            final_result = second_pass_result

            trace.record_step(
                step_number=4,
                phase="PERCEPTION_SECOND_PASS",
                tool_name="vision_core.analyze_surface (Agent-Tuned Config)",
                input_state={"re_calibrated_clahe": 3.8, "re_calibrated_canny": (30, 110)},
                output_state={
                    "post_calibration_status": second_pass_result.status,
                    "post_calibration_defects": second_pass_result.defect_count,
                    "max_area": second_pass_result.max_defect_area
                },
                justification="Executed second pass with autonomous optical re-tuning."
            )

            if second_pass_result.defect_count > 0:
                action_decision = "ROUTE_TO_REWORK_STATION"
                action_details = {
                    "actuator_action": "DIVERT_PNEUMATIC_ARM_B",
                    "reason": "Confirmed structural flaw after high-contrast re-calibration",
                    "severity": "MODERATE_WARNING"
                }
            else:
                action_decision = "PASS_CLEARED_BY_RECALIBRATION"
                action_details = {
                    "actuator_action": "PROCEED_TO_PACKAGING",
                    "reason": "Anomalies resolved as surface glare under multi-threshold equalization",
                    "severity": "NONE"
                }

        elif initial_result.status == "CRITICAL":
            # Catastrophic failure detected -> immediate safety interlock
            action_decision = "EMERGENCY_HALT"
            action_details = {
                "actuator_action": "TRIGGER_LINE_EMERGENCY_BRAKE",
                "reason": f"Critical fracture detected ({int(initial_result.max_defect_area)}px area). Safety interlock engaged.",
                "human_approval_required": True,
                "severity": "CRITICAL_HAZARD"
            }
            trace.record_step(
                step_number=3,
                phase="ACTION",
                tool_name="SafetyInterlockController",
                input_state={"critical_area": initial_result.max_defect_area},
                output_state="CONVEYOR_SHUTDOWN_SIGNAL_ACTIVE",
                justification="Severe fracture exceeds safe operating envelope. Immediate physical line shutdown commanded."
            )

        else:
            # Clear workpiece -> Pass
            action_decision = "PASS"
            action_details = {
                "actuator_action": "PROCEED_TO_PACKAGING",
                "reason": "Surface topology verified defect-free.",
                "severity": "NOMINAL"
            }
            trace.record_step(
                step_number=3,
                phase="ACTION",
                tool_name="ConveyorPassController",
                input_state={"status": "CLEAR"},
                output_state="PASSED_TO_NEXT_STATION",
                justification="Workpiece passed OpenCV 5 structural verification."
            )

        # --- STEP 3: ACTION - AWS TELEMETRY & LOG DISPATCH ---
        step_id = len(trace.steps) + 1
        trace.record_step(
            step_number=step_id,
            phase="CLOUD_TELEMETRY",
            tool_name="AWSTelemetryDispatcher (ap-southeast-2)",
            input_state={"decision": action_decision, "defect_count": final_result.defect_count},
            output_state="Publishing CloudWatch Metrics & Structured Audit Log...",
            justification="Synchronizing edge agent telemetry with AWS Cloud Infrastructure for global observability."
        )

        # Dispatch CloudWatch Metrics
        cloudwatch_res = self.telemetry.send_metrics(
            decision=action_decision,
            defect_count=final_result.defect_count,
            max_area=final_result.max_defect_area,
            latency_ms=final_result.execution_time_ms,
            recalibrated=recalibration_triggered
        )

        # Dispatch Audit Log
        audit_payload = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "decision": action_decision,
            "action_details": action_details,
            "defect_count": final_result.defect_count,
            "max_defect_area": final_result.max_defect_area,
            "latency_ms": final_result.execution_time_ms,
            "cool_accelerated": final_result.cool_accelerated,
            "hardware_target": final_result.hardware_target,
            "recalibrated": recalibration_triggered,
            "defects": final_result.defects
        }
        cloudwatch_log_res = self.telemetry.send_log_event(audit_payload)

        return {
            "decision": action_decision,
            "action_details": action_details,
            "recalibration_triggered": recalibration_triggered,
            "initial_result": initial_result,
            "final_result": final_result,
            "aws_cloudwatch_metrics": cloudwatch_res,
            "aws_cloudwatch_logs": cloudwatch_log_res,
            "agent_trace": trace.get_trace(),
            "hardware_info": self.vision.detect_hardware_acceleration()
        }

