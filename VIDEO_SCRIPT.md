# Video Presentation Script & Voiceover Guide
## OpenCV AI Competition 2026, powered by AWS

**Project**: Autonomous Closed-Loop Visual Inspection System  
**Target Tracks**: Agentic Vision Award & Best Use of COOL Award  
**Team**: VEDA QME-AI  
**Video File**: `demo_presentation.mp4` (1280x720 HD @ 30 FPS)  

---

### ⏱️ Timestamped Voiceover Script (English)

#### [0:00 - 0:15] Title & Introduction
> "Hello judges and OpenCV community! Welcome to our demonstration of the **Autonomous Closed-Loop Visual Inspection System** for the OpenCV AI Competition 2026, powered by AWS.  
> Our system bridges physical edge perception with autonomous agentic decision-making and cloud observability, targeting both the **Agentic Vision Award** and the **Best Use of COOL Award**."

#### [0:15 - 0:40] Problem Statement & Edge Perception
> "In industrial manufacturing, static optical inspection struggles with lighting glare and borderline micro-fractures, causing either false alarms or missed defects.  
> Using **OpenCV 5**, our engine performs adaptive histogram equalization (CLAHE), bilateral denoising, multi-scale Canny edge extraction, and morphological crack quantification—running deterministic inference in under 15 milliseconds."

#### [0:40 - 1:15] Closed-Loop Agentic Vision in Action (Track 1 Highlight)
> "Here is our closed perception-decision-action loop in action:
> 1. When a pristine workpiece is scanned, the agent verifies zero defects and issues a nominal `PASS` command.
> 2. But when a workpiece with borderline micro-cracks arrives, visual evidence alters what the system does next. Rather than guessing, the agent autonomously triggers a **Re-calibration Tool Call**. It modulates its CLAHE contrast from 2.0 to 3.8 and tightens Canny thresholds, executing a targeted second-pass inspection.
> 3. Once the structural flaw is confirmed, the agent commands physical actuator arm B to divert the workpiece to the Rework Station."

#### [1:15 - 1:40] Safety Interlock & Physical Line Halting
> "When a severe fracture exceeding safe structural envelope (>1200 pixels) is detected, the agent triggers an immediate safety interlock: `EMERGENCY_HALT`.  
> It activates the line emergency brake, cuts conveyor power, and requests human supervisor approval, ensuring absolute physical safety."

#### [1:40 - 2:05] AWS CloudWatch Telemetry (Sydney ap-southeast-2)
> "Every single inspection cycle dispatches real-time telemetry to Amazon Web Services in `ap-southeast-2` via `boto3`.  
> We publish custom CloudWatch metrics including DefectCount, Latency, and RecalibrationsTriggered, alongside structured JSON audit logs in `/aws/opencv2026/agentic-inspection` for global enterprise observability."

#### [2:05 - 2:30] Best Use of COOL on AWS Graviton3 (Track 2 Highlight)
> "Finally, our pipeline is optimized for the **Cloud-Optimized OpenCV Library (COOL)** on **AWS Graviton3** (`c7g.xlarge`).  
> Leveraging Arm Neoverse NEON SIMD vectorization, we achieved a **37.8% reduction in latency** (dropping from 14.8 ms to 9.2 ms) and slashed cloud compute costs by **47.1%** per million frames compared to standard x86 instances."

#### [2:30 - 2:45] Conclusion & Open Source Repository
> "All source code, automated test suites, sample images, and one-click run scripts are live on our public GitHub repository. Thank you to the OpenCV Foundation and Amazon Web Services!"

---

### 🇧🇩 Timestamped Voiceover Script (বাংলা ভার্সন)

- **[0:00 - 0:25] ভূমিকা**: "নমস্কার বিচারকমণ্ডলী! এটি OpenCV AI Competition 2026-এর জন্য আমাদের অটোনোমাস ক্লোজড-লুপ ভিজ্যুয়াল ইন্সপেকশন প্রজেক্ট। আমরা OpenCV 5 এবং AWS ক্লাউড ব্যবহার করে ইন্ডাস্ট্রিয়াল ডিফেক্ট ডিটেকশন ও অটোমেশন তৈরি করেছি।"
- **[0:25 - 1:10] এজেন্টিক ভিশন ও রি-ক্যালিব্রেশন লুপ**: "আমাদের এজেন্ট শুধু ইমেজ দেখে থেমে থাকে না; ভিস্যুয়াল রেজাল্ট দেখে পরবর্তী টুল কল নিয়ন্ত্রণ করে। কোনো পার্টে সামান্য মাইক্রো-ক্র্যাক পেলে এজেন্ট নিজে থেকেই কনট্রাস্ট ও থ্রেশহোল্ড রি-টিউন করে সেকেন্ড-পাস রি-ইন্সপেকশন চালায় এবং ডিফেক্ট নিশ্চিত করে রি-ওয়ার্ক স্টেশনে পাঠায়।"
- **[1:10 - 1:35] সেফটি ইন্টারলক ও ইমার্জেন্সি হল্ট**: "মারাত্মক ফাটল ডিটেক্ট হলে এজেন্ট স্বয়ংক্রিয়ভাবে ফ্যাক্টরি লাইনে ইমার্জেন্সি ব্রেক প্রয়োগ করে কনভেয়ার বন্ধ করে দেয়।"
- **[1:35 - 2:10] AWS ক্লাউড ও Graviton COOL এক্সেলারেশন**: "প্রতিটি রেজাল্ট সরাসরি AWS Sydney রিজিয়নের CloudWatch-এ স্ট্রিম হচ্ছে। এছাড়াও AWS Graviton3 প্রসেসরে Arm NEON ভেক্টরাইজেশন ব্যবহারের ফলে ৩৭.৮% দ্রুত প্রসেসিং এবং ৪৭.১% ক্লাউড খরচ হ্রাস পেয়েছে।"
