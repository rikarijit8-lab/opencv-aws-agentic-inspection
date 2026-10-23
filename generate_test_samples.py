"""
generate_test_samples.py - Synthetic Industrial Workpiece Sample Generator
Generates realistic workpiece samples for instant testing:
1. sample_pristine.png: Defect-free brushed metal surface.
2. sample_marginal_crack.png: Workpiece with fine micro-cracks triggering Agent Re-calibration.
3. sample_critical_fracture.png: Workpiece with severe fracture triggering Emergency Halt.
4. sample_low_contrast_glare.png: Optical glare anomaly resolved by adaptive CLAHE equalization.
"""

import os
import cv2
import numpy as np


def generate_brushed_metal_base(width: int = 640, height: int = 480) -> np.ndarray:
    """Generate a realistic brushed aluminum/steel industrial workpiece texture."""
    base = np.full((height, width), 165, dtype=np.uint8)
    # Add subtle horizontal brushing grain
    noise = np.random.normal(0, 7, (height, width)).astype(np.float32)
    brushed = cv2.GaussianBlur(noise, (17, 1), 0)
    img = np.clip(base + brushed, 0, 255).astype(np.uint8)
    return img


def create_pristine_sample(output_path: str):
    img = generate_brushed_metal_base()
    cv2.imwrite(output_path, cv2.cvtColor(img, cv2.COLOR_GRAY2BGR))


def create_marginal_crack_sample(output_path: str):
    img = generate_brushed_metal_base()
    # Draw hairline micro-cracks (faint contrast, requiring high-sensitivity re-calibration)
    pts = np.array([[240, 180], [260, 205], [275, 230], [295, 255]], np.int32)
    cv2.polylines(img, [pts], isClosed=False, color=110, thickness=2, lineType=cv2.LINE_AA)
    
    # Secondary tiny hairline
    pts2 = np.array([[380, 290], [395, 305], [410, 315]], np.int32)
    cv2.polylines(img, [pts2], isClosed=False, color=115, thickness=2, lineType=cv2.LINE_AA)
    
    cv2.imwrite(output_path, cv2.cvtColor(img, cv2.COLOR_GRAY2BGR))


def create_critical_fracture_sample(output_path: str):
    img = generate_brushed_metal_base()
    # Draw severe structural fracture with heavy cavity
    pts = np.array([
        [180, 140], [215, 185], [245, 200], [290, 260],
        [330, 295], [370, 350], [405, 400]
    ], np.int32)
    cv2.polylines(img, [pts], isClosed=False, color=20, thickness=7, lineType=cv2.LINE_AA)
    
    # Deep fracture pits
    cv2.circle(img, (290, 260), 24, 15, -1)
    cv2.circle(img, (215, 185), 18, 15, -1)
    cv2.circle(img, (370, 350), 20, 20, -1)
    
    cv2.imwrite(output_path, cv2.cvtColor(img, cv2.COLOR_GRAY2BGR))


def create_low_contrast_glare_sample(output_path: str):
    img = generate_brushed_metal_base()
    # Add optical glare hotspot (washout)
    glare = np.zeros_like(img, dtype=np.float32)
    cv2.circle(glare, (320, 240), 100, 70, -1)
    glare = cv2.GaussianBlur(glare, (89, 89), 0)
    img = np.clip(img.astype(np.float32) + glare, 0, 255).astype(np.uint8)
    
    cv2.imwrite(output_path, cv2.cvtColor(img, cv2.COLOR_GRAY2BGR))


def main():
    os.makedirs("samples", exist_ok=True)
    create_pristine_sample("samples/sample_pristine.png")
    create_marginal_crack_sample("samples/sample_marginal_crack.png")
    create_critical_fracture_sample("samples/sample_critical_fracture.png")
    create_low_contrast_glare_sample("samples/sample_low_contrast_glare.png")
    print("Test samples generated successfully in ./samples/")


if __name__ == "__main__":
    main()

