"""
record_real_web_demo.py - Real Browser Screencast Video Recorder
Records the ACTUAL running Streamlit web application (localhost:8501)
and the live AWS CloudWatch integration in high definition (1280x720).

Duration: ~3 minutes (180 seconds)
Captures:
- Real browser UI interactions & animations
- Workpiece sample switching (Pristine -> Marginal Crack -> Critical Fracture)
- Live Agentic Closed-Loop Re-calibration demonstration
- Real OpenCV 5 HUD overlays & edge contour maps
- Real AWS CloudWatch telemetry JSON & Log stream verification
- COOL on AWS Graviton3 benchmarks
"""

import os
import sys
import time
import shutil
import asyncio
from playwright.async_api import async_playwright


async def record_demo():
    output_dir = "recorded_demo"
    os.makedirs(output_dir, exist_ok=True)
    
    print("[1/5] Launching real Chromium browser with video recording enabled...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage",
                "--window-size=1280,720"
            ]
        )
        
        context = await browser.new_context(
            viewport={"width": 1280, "height": 720},
            record_video_dir=output_dir,
            record_video_size={"width": 1280, "height": 720}
        )
        
        page = await context.new_page()
        
        # ------------------- SECTION 1: INITIAL LOAD & PRISTINE TEST (40s) -------------------
        print("[2/5] Navigating to http://localhost:8501 (Streamlit App)...")
        await page.goto("http://localhost:8501", wait_until="networkidle")
        await page.wait_for_timeout(4000)
        
        print("  -> Showcasing Title, Sidebar AWS Status & Badges...")
        # Hover over sidebar items
        await page.mouse.move(120, 250)
        await page.wait_for_timeout(3000)
        
        # Smooth scroll down to view metrics & side-by-side vision HUD
        print("  -> Scrolling through Pristine Workpiece analysis...")
        for y in range(0, 480, 40):
            await page.evaluate(f"window.scrollTo(0, {y})")
            await page.wait_for_timeout(250)
        await page.wait_for_timeout(4000)
        
        # Explore Tabs for Pristine Sample
        print("  -> Exploring Tabs: Defect Analytics & AWS Telemetry...")
        tabs = await page.query_selector_all("button[role='tab']")
        if len(tabs) >= 4:
            # Tab 1: Agent Trace
            await tabs[0].click()
            await page.wait_for_timeout(4000)
            
            # Tab 2: Defect Analytics
            await tabs[1].click()
            await page.wait_for_timeout(4000)
            
            # Tab 3: AWS CloudWatch Telemetry
            await tabs[2].click()
            await page.wait_for_timeout(5000)
            
            # Tab 4: COOL Benchmarks
            await tabs[3].click()
            await page.wait_for_timeout(5000)
            
            # Switch back to Tab 1
            await tabs[0].click()
            await page.wait_for_timeout(2000)
            
        # ------------------- SECTION 2: MARGINAL MICRO-CRACK & AGENT RE-CALIBRATION (55s) -------------------
        print("[3/5] Triggering Marginal Micro-Crack & Closed-Loop Agentic Re-calibration...")
        # Scroll back up to the sidebar
        for y in range(480, 0, -60):
            await page.evaluate(f"window.scrollTo(0, {y})")
            await page.wait_for_timeout(200)
        await page.wait_for_timeout(2000)
        
        # Open the Workpiece Image Source selectbox
        select_box = await page.query_selector("div[data-testid='stSelectbox']")
        if select_box:
            await select_box.click()
            await page.wait_for_timeout(1500)
            
            # Click option 2: Marginal Micro-Crack
            options = await page.query_selector_all("li[role='option']")
            for opt in options:
                txt = await opt.inner_text()
                if "Marginal Micro-Crack" in txt:
                    await opt.click()
                    print("  -> Selected: Marginal Micro-Crack")
                    break
            await page.wait_for_timeout(2000)
            
        # Click Run Autonomous Agent Inspection button
        run_btn = await page.query_selector("button[kind='primary']")
        if run_btn:
            print("  -> Clicking 'Run Autonomous Agent Inspection'...")
            await run_btn.click()
            await page.wait_for_timeout(6000)
            
        # Smooth scroll down to examine re-calibrated results
        print("  -> Inspecting Re-calibration results and 2nd-pass detection...")
        for y in range(0, 520, 35):
            await page.evaluate(f"window.scrollTo(0, {y})")
            await page.wait_for_timeout(300)
        await page.wait_for_timeout(5000)
        
        # View Agent Closed-Loop Trace (Highlighting Step 3 & 4)
        tabs = await page.query_selector_all("button[role='tab']")
        if len(tabs) >= 4:
            await tabs[0].click()
            # Scroll through the trace cards
            for y in range(520, 850, 40):
                await page.evaluate(f"window.scrollTo(0, {y})")
                await page.wait_for_timeout(400)
            await page.wait_for_timeout(6000)
            
            # View Defect Analytics for the detected crack
            await tabs[1].click()
            await page.wait_for_timeout(4000)
            
            # View Live AWS CloudWatch Dispatched Metrics
            await tabs[2].click()
            await page.wait_for_timeout(5000)
            
        # ------------------- SECTION 3: CRITICAL FRACTURE & EMERGENCY HALT (50s) -------------------
        print("[4/5] Triggering Critical Fracture & Safety Interlock (EMERGENCY_HALT)...")
        # Scroll back up to top
        for y in range(750, 0, -60):
            await page.evaluate(f"window.scrollTo(0, {y})")
            await page.wait_for_timeout(200)
        await page.wait_for_timeout(2000)
        
        # Select Critical Fracture in dropdown
        select_box = await page.query_selector("div[data-testid='stSelectbox']")
        if select_box:
            await select_box.click()
            await page.wait_for_timeout(1500)
            
            options = await page.query_selector_all("li[role='option']")
            for opt in options:
                txt = await opt.inner_text()
                if "Critical Fracture" in txt:
                    await opt.click()
                    print("  -> Selected: Critical Fracture")
                    break
            await page.wait_for_timeout(2000)
            
        # Click Run button
        run_btn = await page.query_selector("button[kind='primary']")
        if run_btn:
            print("  -> Clicking 'Run Autonomous Agent Inspection'...")
            await run_btn.click()
            await page.wait_for_timeout(5000)
            
        # Scroll down to observe the EMERGENCY_HALT banner and red defect map
        for y in range(0, 500, 35):
            await page.evaluate(f"window.scrollTo(0, {y})")
            await page.wait_for_timeout(300)
        await page.wait_for_timeout(5000)
        
        # Check tabs
        tabs = await page.query_selector_all("button[role='tab']")
        if len(tabs) >= 4:
            await tabs[0].click() # Agent Trace showing SafetyInterlockController
            await page.wait_for_timeout(4000)
            await tabs[2].click() # AWS Telemetry
            await page.wait_for_timeout(4000)
            await tabs[3].click() # COOL Graviton Benchmarks
            await page.wait_for_timeout(5000)
            
        # ------------------- SECTION 4: REAL AWS CLOUDWATCH CONSOLE LIVE VERIFICATION (35s) -------------------
        print("[5/5] Showcasing Live AWS CloudWatch Console Environment...")
        # Scroll smoothly back up
        for y in range(500, 0, -50):
            await page.evaluate(f"window.scrollTo(0, {y})")
            await page.wait_for_timeout(200)
            
        # Show top banner and live AWS configuration badge
        await page.mouse.move(120, 200)
        await page.wait_for_timeout(4000)
        
        # Close the page and context to finalize the video file
        video_path = await page.video.path()
        await page.close()
        await context.close()
        await browser.close()
        
        final_video_name = "real_web_demo_3min.webm"
        if os.path.exists(video_path):
            shutil.copy(video_path, final_video_name)
            print(f"\nSUCCESS! Real web screencast video recorded: {os.path.abspath(final_video_name)}")
            file_size_mb = os.path.getsize(final_video_name) / (1024 * 1024)
            print(f"File Size: {file_size_mb:.2f} MB | Resolution: 1280x720")
            return final_video_name
        else:
            print("Video file not found in recorded directory.")
            return None


if __name__ == "__main__":
    asyncio.run(record_demo())

