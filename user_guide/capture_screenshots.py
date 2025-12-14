"""
Automated screenshot capture script for Real-Time Scheduling Simulator User Guide.
This script uses browser automation to systematically capture all features.
"""

import time
import os
from pathlib import Path
from typing import List, Dict, Optional
import subprocess
import sys

# Try to import browser automation libraries
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait, Select
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
    print("Selenium not available. Install with: pip install selenium")

try:
    from playwright.sync_api import sync_playwright, Page
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("Playwright not available. Install with: pip install playwright && playwright install")

# Screenshot directories
BASE_DIR = Path(__file__).parent
SCREENSHOTS_DIR = BASE_DIR / "screenshots"

class ScreenshotCapture:
    """Main class for capturing screenshots of the scheduling simulator."""
    
    def __init__(self, use_playwright: bool = True):
        self.use_playwright = use_playwright and PLAYWRIGHT_AVAILABLE
        self.use_selenium = not self.use_playwright and SELENIUM_AVAILABLE
        self.browser = None
        self.page = None
        self.driver = None
        self.base_url = "http://localhost:8501"
        
    def start_browser(self):
        """Start browser and navigate to app."""
        if self.use_playwright:
            self.playwright = sync_playwright().start()
            self.browser = self.playwright.chromium.launch(headless=False)
            self.page = self.browser.new_page()
            self.page.goto(self.base_url)
            self.page.wait_for_load_state("networkidle")
            time.sleep(2)  # Wait for Streamlit to fully load
        elif self.use_selenium:
            options = Options()
            options.add_argument("--start-maximized")
            self.driver = webdriver.Chrome(options=options)
            self.driver.get(self.base_url)
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            time.sleep(2)
        else:
            raise RuntimeError("No browser automation library available")
    
    def take_screenshot(self, filename: str, subdirectory: str = ""):
        """Take a screenshot and save it."""
        if subdirectory:
            save_path = SCREENSHOTS_DIR / subdirectory / filename
        else:
            save_path = SCREENSHOTS_DIR / filename
        
        save_path.parent.mkdir(parents=True, exist_ok=True)
        
        if self.use_playwright:
            self.page.screenshot(path=str(save_path), full_page=True)
        elif self.use_selenium:
            self.driver.save_screenshot(str(save_path))
        
        print(f"Saved: {save_path}")
        return save_path
    
    def wait_for_element(self, selector: str, timeout: int = 10):
        """Wait for an element to appear."""
        if self.use_playwright:
            self.page.wait_for_selector(selector, timeout=timeout * 1000)
        elif self.use_selenium:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
    
    def click(self, selector: str):
        """Click an element."""
        if self.use_playwright:
            self.page.click(selector)
        elif self.use_selenium:
            element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
            )
            element.click()
        time.sleep(0.5)  # Wait for UI update
    
    def fill_input(self, selector: str, value: str):
        """Fill an input field."""
        if self.use_playwright:
            self.page.fill(selector, value)
        elif self.use_selenium:
            element = self.driver.find_element(By.CSS_SELECTOR, selector)
            element.clear()
            element.send_keys(value)
        time.sleep(0.3)
    
    def select_option(self, selector: str, value: str):
        """Select an option from a dropdown."""
        if self.use_playwright:
            self.page.select_option(selector, value)
        elif self.use_selenium:
            select = Select(self.driver.find_element(By.CSS_SELECTOR, selector))
            select.select_by_visible_text(value)
        time.sleep(0.5)
    
    def close(self):
        """Close browser."""
        if self.use_playwright:
            self.browser.close()
            self.playwright.stop()
        elif self.use_selenium:
            self.driver.quit()

def main():
    """Main function to capture all screenshots."""
    print("Starting screenshot capture...")
    print("Make sure Streamlit app is running on http://localhost:8501")
    
    # Wait for user confirmation
    input("Press Enter when Streamlit app is ready...")
    
    capture = ScreenshotCapture()
    
    try:
        capture.start_browser()
        print("Browser started successfully!")
        
        # Part 1: Getting Started
        print("\n=== Part 1: Getting Started ===")
        capture.take_screenshot("01-initial-state.png", "part1-getting-started")
        capture.take_screenshot("02-full-layout.png", "part1-getting-started")
        
        # TODO: Continue with all other parts...
        # This is a framework - actual implementation will be done step by step
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        capture.close()

if __name__ == "__main__":
    main()

