"""
test_pipeline.py - Automated Unit & Integration Tests
OpenCV AI Competition 2026 (Powered by AWS)

Verifies:
1. OpenCV 5 Vision Core defect detection accuracy across workpieces.
2. Closed-Loop Agentic Re-calibration trigger on marginal anomalies.
3. Actuator commands (PASS, ROUTE_TO_REWORK_STATION, EMERGENCY_HALT).
4. Telemetry payload formatting for AWS CloudWatch (ap-southeast-2).
"""

import os
import cv2
import pytest
import numpy as np

from vision_core import IndustrialVisionCore, InspectionConfig
from agent_pipeline import AgenticInspectionPipeline, AgentExecutionTrace
import generate_test_samples


@pytest.fixture(scope="session", autouse=True)
def ensure_samples():
    """Ensure sample workpiece images exist before running tests."""
    generate_test_samples.main()


def test_pristine_workpiece_pass():
    """Pristine workpiece must be evaluated as nominal CLEAR and PASS."""
    pipeline = AgenticInspectionPipeline()
    img = cv2.imread("samples/sample_pristine.png")
    assert img is not None, "Failed to load sample_pristine.png"

    result = pipeline.execute_inspection_cycle(img)
    assert result["decision"] == "PASS"
    assert result["recalibration_triggered"] is False
    assert result["final_result"].defect_count == 0


def test_marginal_crack_triggers_agentic_recalibration():
    """Marginal micro-crack must trigger the Closed-Loop Agentic Re-calibration pass."""
    pipeline = AgenticInspectionPipeline()
    img = cv2.imread("samples/sample_marginal_crack.png")
    assert img is not None, "Failed to load sample_marginal_crack.png"

    result = pipeline.execute_inspection_cycle(img)
    assert result["recalibration_triggered"] is True, "Agent failed to trigger closed-loop re-calibration!"
    assert result["decision"] == "ROUTE_TO_REWORK_STATION"
    assert result["final_result"].defect_count >= 1

    # Verify agent trace contains both initial and second-pass perception
    trace_phases = [s["phase"] for s in result["agent_trace"]]
    assert "PERCEPTION" in trace_phases
    assert "DECISION_ORCHESTRATION" in trace_phases
    assert "PERCEPTION_SECOND_PASS" in trace_phases
    assert "CLOUD_TELEMETRY" in trace_phases


def test_critical_fracture_triggers_emergency_halt():
    """Catastrophic fracture must trigger immediate EMERGENCY_HALT safety interlock."""
    pipeline = AgenticInspectionPipeline()
    img = cv2.imread("samples/sample_critical_fracture.png")
    assert img is not None, "Failed to load sample_critical_fracture.png"

    result = pipeline.execute_inspection_cycle(img)
    assert result["decision"] == "EMERGENCY_HALT"
    assert result["action_details"]["actuator_action"] == "TRIGGER_LINE_EMERGENCY_BRAKE"
    assert result["final_result"].max_defect_area > 1000.0


def test_hardware_acceleration_detection():
    """Hardware detector must return OpenCV version and architecture flags."""
    core = IndustrialVisionCore()
    hw = core.detect_hardware_acceleration()
    assert "opencv_version" in hw
    assert "architecture" in hw
    assert "cool_library_mode" in hw


if __name__ == "__main__":
    pytest.main(["-v", __file__])

