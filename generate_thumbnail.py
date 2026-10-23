"""
generate_thumbnail.py - Devpost Submission 3:2 Ratio Master Thumbnail Generator
OpenCV AI Competition 2026, powered by AWS

Creates: thumbnail.png (1200x800 px, 3:2 Aspect Ratio)
Designed specifically to stand out to Devpost hackathon judges:
- Dual Track Badges: [Agentic Vision] [Best Use of COOL]
- Industrial Defect Detection HUD with OpenCV 5
- Closed-Loop Decision Flow & AWS CloudWatch Telemetry
"""

import cv2
import numpy as np


def create_gradient_backdrop(width=1200, height=800):
    """Generate high-tech dark steel blue industrial gradient."""
    backdrop = np.zeros((height, width, 3), dtype=np.uint8)
    for y in range(height):
        ratio = y / float(height)
        # Gradient from deep dark navy (12, 16, 26) to midnight slate (24, 32, 48)
        b = int(26 + (ratio * 22))
        g = int(16 + (ratio * 16))
        r = int(12 + (ratio * 12))
        backdrop[y, :] = (b, g, r)
    return backdrop


def draw_hud_box(img, x, y, w, h, title="", border_color=(60, 75, 105), fill_color=(18, 24, 38)):
    """Draw futuristic HUD card container."""
    cv2.rectangle(img, (x, y), (x + w, y + h), fill_color, -1)
    cv2.rectangle(img, (x, y), (x + w, y + h), border_color, 2)
    
    # Corner accent ticks
    tick = 10
    cv2.line(img, (x, y), (x + tick, y), (0, 164, 239), 3)
    cv2.line(img, (x, y), (x, y + tick), (0, 164, 239), 3)
    cv2.line(img, (x + w, y), (x + w - tick, y), (0, 164, 239), 3)
    cv2.line(img, (x + w, y), (x + w, y + tick), (0, 164, 239), 3)
    cv2.line(img, (x, y + h), (x + tick, y + h), (0, 164, 239), 3)
    cv2.line(img, (x, y + h), (x, y + h - tick), (0, 164, 239), 3)
    cv2.line(img, (x + w, y + h), (x + w - tick, y + h), (0, 164, 239), 3)
    cv2.line(img, (x + w, y + h), (x + w, y + h - tick), (0, 164, 239), 3)

    if title:
        cv2.rectangle(img, (x, y), (x + w, y + 32), (28, 38, 56), -1)
        cv2.line(img, (x, y + 32), (x + w, y + 32), border_color, 1)
        cv2.putText(img, title, (x + 14, y + 22), cv2.FONT_HERSHEY_DUPLEX, 0.50, (230, 230, 230), 1, cv2.LINE_AA)


def generate_thumbnail():
    W, H = 1200, 800
    img = create_gradient_backdrop(W, H)

    # 1. TOP HEADER BANNER
    cv2.rectangle(img, (0, 0), (W, 85), (15, 20, 32), -1)
    cv2.line(img, (0, 85), (W, 85), (0, 164, 239), 2)

    cv2.putText(img, "OPENCV AI COMPETITION 2026", (36, 40), cv2.FONT_HERSHEY_DUPLEX, 0.95, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(img, "POWERED BY AMAZON WEB SERVICES (AWS) | TEAM VEDA QME-AI", (38, 68), cv2.FONT_HERSHEY_SIMPLEX, 0.50, (0, 200, 255), 1, cv2.LINE_AA)

    # Competition Badges (Top Right)
    cv2.rectangle(img, (W - 480, 22), (W - 270, 62), (212, 120, 0), -1)
    cv2.putText(img, "AGENTIC VISION", (W - 460, 48), cv2.FONT_HERSHEY_SIMPLEX, 0.52, (255, 255, 255), 2, cv2.LINE_AA)

    cv2.rectangle(img, (W - 250, 22), (W - 36, 62), (0, 102, 204), -1)
    cv2.putText(img, "COOL ON GRAVITON", (W - 240, 48), cv2.FONT_HERSHEY_SIMPLEX, 0.52, (255, 255, 255), 2, cv2.LINE_AA)

    # 2. MAIN TITLE HERO TEXT
    cv2.putText(img, "Autonomous Closed-Loop Visual Inspection", (36, 135), cv2.FONT_HERSHEY_DUPLEX, 1.25, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(img, "Perception -> Decision Orchestration -> Closed-Loop Re-tuning -> AWS CloudWatch & Actuators", 
                (38, 170), cv2.FONT_HERSHEY_SIMPLEX, 0.52, (180, 210, 235), 1, cv2.LINE_AA)

    # 3. LEFT PANEL: OpenCV 5 DEFECT PERCEPTION HUD (Real Sample Visualization)
    card_w, card_h = 540, 340
    card_x, card_y = 36, 195
    draw_hud_box(img, card_x, card_y, card_w, card_h, "OPENCV 5 CORE | HIGH-PRECISION DEFECT SEGMENTATION")

    # Load actual defect workpiece sample
    try:
        sample = cv2.imread("samples/sample_marginal_crack.png")
        if sample is not None:
            sample_resized = cv2.resize(sample, (520, 280))
            
            # Apply Defect Annotation HUD
            cv2.rectangle(sample_resized, (170, 95), (280, 210), (0, 165, 255), 2)
            cv2.putText(sample_resized, "MICRO-CRACK #1 (514px)", (165, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.50, (0, 165, 255), 2, cv2.LINE_AA)
            cv2.putText(sample_resized, "SEVERITY: 0.64 (MARGINAL)", (165, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.40, (0, 220, 255), 1, cv2.LINE_AA)
            
            cv2.rectangle(sample_resized, (320, 180), (430, 245), (0, 255, 255), 2)
            cv2.putText(sample_resized, "HAIRLINE #2 (153px)", (320, 172), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 255), 1, cv2.LINE_AA)
            
            # Top mini status overlay
            cv2.rectangle(sample_resized, (0, 0), (520, 26), (20, 20, 20), -1)
            cv2.putText(sample_resized, "CLAHE 3.8 | BILATERAL 75 | CANNY 30/110 | GRAVITON SIMD", (10, 18), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (0, 255, 128), 1, cv2.LINE_AA)
            
            img[card_y + 40:card_y + 40 + 280, card_x + 10:card_x + 10 + 520] = sample_resized
    except Exception as e:
        pass

    # 4. RIGHT PANEL: AGENTIC WORKFLOW & AWS CLOUD ARCHITECTURE
    r_x, r_y = 610, 195
    r_w, r_h = 554, 340
    draw_hud_box(img, r_x, r_y, r_w, r_h, "AGENT PERCEPTION-DECISION-ACTION LOOP & AWS ARCHITECTURE")

    # Workflow Steps Cards
    steps = [
        ("1. Optical Perception", "OpenCV 5 extracts micro-cracks & contour geometries (14.8 ms).", (0, 164, 239)),
        ("2. Closed-Loop Re-tuning", "Visual output triggers sensor retuning (CLAHE 2.0->3.8, Canny 30/110).", (255, 165, 0)),
        ("3. Physical Actuator Action", "Commands Rework Diverter Arm B or triggers EMERGENCY HALT.", (0, 220, 100)),
        ("4. AWS Cloud Telemetry", "Real-time CloudWatch Metrics & Logs in Sydney (ap-southeast-2).", (180, 100, 255))
    ]

    for i, (stitle, sdesc, color) in enumerate(steps):
        sy = r_y + 45 + (i * 68)
        cv2.rectangle(img, (r_x + 16, sy), (r_x + r_w - 16, sy + 56), (22, 28, 42), -1)
        cv2.rectangle(img, (r_x + 16, sy), (r_x + r_w - 16, sy + 56), (40, 52, 72), 1)
        cv2.rectangle(img, (r_x + 16, sy), (r_x + 22, sy + 56), color, -1)
        
        cv2.putText(img, stitle, (r_x + 34, sy + 22), cv2.FONT_HERSHEY_DUPLEX, 0.48, color, 1, cv2.LINE_AA)
        cv2.putText(img, sdesc, (r_x + 34, sy + 44), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (210, 210, 210), 1, cv2.LINE_AA)

    # 5. BOTTOM ROW: THREE KEY ADVANTAGE METRIC CARDS
    card_data = [
        ("AWS GRAVITON3 + COOL", "37.8% FASTER", "9.2 ms Frame Latency (vs 14.8 ms x86)", (0, 200, 100)),
        ("CLOUD COST EFFICIENCY", "47.1% SAVINGS", "$0.37 per 1M Frames on c7g.xlarge", (0, 220, 255)),
        ("SAFETY & RELIABILITY", "CLOSED-LOOP HALT", "Automatic Millisecond Emergency Brake", (0, 140, 255))
    ]

    b_y = 560
    b_w = 368
    for i, (m_tag, m_big, m_sub, m_col) in enumerate(card_data):
        bx = 36 + (i * 398)
        draw_hud_box(img, bx, b_y, b_w, 155, m_tag, border_color=(45, 60, 85))
        
        cv2.putText(img, m_big, (bx + 20, b_y + 85), cv2.FONT_HERSHEY_DUPLEX, 0.95, m_col, 2, cv2.LINE_AA)
        cv2.putText(img, m_sub, (bx + 20, b_y + 125), cv2.FONT_HERSHEY_SIMPLEX, 0.44, (200, 200, 200), 1, cv2.LINE_AA)

    # 6. FOOTER BRANDING STRIP
    cv2.rectangle(img, (0, H - 50), (W, H), (15, 20, 30), -1)
    cv2.line(img, (0, H - 50), (W, H - 50), (35, 45, 65), 1)
    cv2.putText(img, "GitHub: rikarijit8-lab/opencv-aws-agentic-inspection", (36, H - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.46, (160, 160, 160), 1, cv2.LINE_AA)
    cv2.putText(img, "OpenCV 5 Core  |  AWS CloudWatch (ap-southeast-2)  |  COOL on AWS Graviton  |  Streamlit", 
                (W - 680, H - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.44, (0, 200, 100), 1, cv2.LINE_AA)

    # Save to disk
    output_path = "thumbnail.png"
    cv2.imwrite(output_path, img)
    print(f"Master Thumbnail generated successfully: {output_path} (1200x800, 3:2 Ratio)")


if __name__ == "__main__":
    generate_thumbnail()
