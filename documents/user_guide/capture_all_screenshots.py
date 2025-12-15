"""
Comprehensive automated screenshot capture using Playwright.
This script systematically captures all screenshots, ensuring correct state.
"""

import asyncio
from playwright.async_api import async_playwright, Page, Browser
from pathlib import Path
import json
from typing import Dict, List, Optional, Callable
import socket
import urllib.request
import urllib.error
import sys
import argparse

BASE_URL = "http://localhost:8501"
SCREENSHOTS_DIR = Path(__file__).parent / "screenshots"
STATS = {"total": 0, "replaced": 0, "new": 0, "errors": 0}

# Part mapping for resume functionality
PARTS = {
    1: ("Part 1: Getting Started", "capture_part1_getting_started"),
    2: ("Part 2: Basic Algorithms", "capture_part2_basic_algorithms"),
    3: ("Part 3: Server Algorithms", "capture_part3_server_algorithms"),
    4: ("Part 4: Precedence-Constrained", "capture_part4_precedence"),
    5: ("Part 5: Aperiodic Scheduling", "capture_part5_aperiodic"),
    6: ("Part 6: Overload Handling", "capture_part6_overload"),
    7: ("Part 7: Resource Sharing", "capture_part7_resource_sharing"),
}


def check_port_open(host: str, port: int, timeout: float = 2.0) -> bool:
    """Check if a port is open and accepting connections."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except:
        return False


def check_url_accessible(url: str, timeout: float = 3.0) -> bool:
    """Check if a URL is accessible."""
    try:
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0')
        response = urllib.request.urlopen(req, timeout=timeout)
        return response.getcode() == 200
    except (urllib.error.URLError, socket.timeout, Exception):
        return False


async def wait_for_stable(page: Page, timeout: int = 2000):
    """Wait for UI to stabilize."""
    await page.wait_for_timeout(timeout)
    try:
        await page.wait_for_selector('[data-testid="stApp"]', timeout=1000)
    except:
        pass


async def wait_for_network_idle(page: Page, timeout: int = 5000):
    """Wait for network to be idle (no pending requests)."""
    try:
        await page.wait_for_load_state("networkidle", timeout=timeout)
    except:
        pass
    await wait_for_stable(page, 1000)


async def wait_for_element_visible(page: Page, selector: str, timeout: int = 5000):
    """Wait for an element to be visible."""
    try:
        await page.wait_for_selector(selector, state="visible", timeout=timeout)
    except:
        pass
    await wait_for_stable(page, 500)


async def ensure_no_modals(page: Page):
    """Ensure no modals/dialogs are open."""
    # Check for dialogs
    dialogs = await page.locator('[role="dialog"]').count()
    if dialogs > 0:
        await page.keyboard.press('Escape')
        await wait_for_stable(page, 1000)
    # Double check
    dialogs = await page.locator('[role="dialog"]').count()
    if dialogs > 0:
        # Try clicking outside
        await page.click('body', position={'x': 10, 'y': 10})
        await wait_for_stable(page, 1000)


async def select_category(page: Page, category: str):
    """Select category from dropdown."""
    await ensure_no_modals(page)
    await wait_for_network_idle(page, 3000)
    
    # Wait for category dropdown to be visible - try multiple selectors
    category_selectors = [
        '[aria-label*="Category"]',
        'selectbox:has-text("Category")',
        'div:has-text("Category")',
    ]
    
    category_select = None
    for selector in category_selectors:
        locator = page.locator(selector).first
        if await locator.count() > 0:
            category_select = locator
            break
    
    if not category_select:
        raise Exception("Category dropdown not found")
    
    await wait_for_stable(page, 1000)
    
    # Get current category text - try multiple ways
    current_text = await category_select.text_content()
    if not current_text or current_text.strip() == "":
        # Try getting text from inner elements
        inner_text = await category_select.inner_text()
        if inner_text:
            current_text = inner_text
    
    # Also try getting the value from the selectbox
    if not current_text or current_text.strip() == "":
        try:
            # Streamlit selectbox might have the value in a different element
            parent = category_select.locator('..')
            current_text = await parent.text_content()
        except:
            pass
    
    if current_text and category.lower() in current_text.lower():
        # Already selected
        print(f"    Category already selected: {current_text.strip()}")
        await wait_for_network_idle(page, 2000)
        return
    
    # Click to open dropdown
    await category_select.click()
    await wait_for_stable(page, 1500)
    
    # Wait for dropdown list to appear
    try:
        await page.wait_for_selector('[role="listbox"], [role="option"]', state='visible', timeout=5000)
    except:
        pass
    
    await wait_for_stable(page, 1000)
    
    # Find and click the option
    options = page.locator('[role="option"]')
    count = await options.count()
    
    if count == 0:
        await wait_for_stable(page, 2000)
        options = page.locator('[role="option"]')
        count = await options.count()
    
    # Try exact match first
    for i in range(count):
        text = await options.nth(i).text_content()
        if not text:
            text = await options.nth(i).inner_text()
        if text:
            text = text.strip()
            if category == text or category.lower() == text.lower():
                await options.nth(i).click()
                # Wait for category to change and algorithm dropdown to update
                await wait_for_network_idle(page, 5000)
                await wait_for_stable(page, 2000)
                # Verify the category was actually selected - wait a bit and check again
                await wait_for_stable(page, 1000)
                # Don't fail if we can't verify - Streamlit might update async
                return
    
    # Try partial match
    for i in range(count):
        text = await options.nth(i).text_content()
        if not text:
            text = await options.nth(i).inner_text()
        if text and category.lower() in text.lower():
            await options.nth(i).click()
            await wait_for_network_idle(page, 5000)
            await wait_for_stable(page, 2000)
            return
    
    # Debug: print available options
    available = []
    for i in range(count):
        text = await options.nth(i).text_content()
        if not text:
            text = await options.nth(i).inner_text()
        if text:
            available.append(text.strip())
    raise Exception(f"Category '{category}' not found. Available: {available}")


async def select_algorithm(page: Page, algorithm: str):
    """Select algorithm from dropdown."""
    await ensure_no_modals(page)
    await wait_for_network_idle(page, 3000)
    
    # Wait for algorithm dropdown to be visible - make sure we get the Algorithm dropdown, not Category
    # The Algorithm dropdown should be the second selectbox or the one with "Algorithm" in aria-label
    algo_selectors = [
        '[aria-label*="Algorithm"]:not([aria-label*="Category"])',
        'selectbox:has-text("Algorithm")',
    ]
    
    algo_select = None
    for selector in algo_selectors:
        locators = page.locator(selector)
        count = await locators.count()
        if count > 0:
            # Get the one that's NOT the category dropdown
            for i in range(count):
                loc = locators.nth(i)
                label = await loc.get_attribute('aria-label')
                if label and 'Algorithm' in label and 'Category' not in label:
                    algo_select = loc
                    break
            if algo_select:
                break
    
    # Fallback: get all selectboxes and find the Algorithm one
    if not algo_select:
        all_selects = page.locator('[aria-label*="Algorithm"], [aria-label*="Category"]')
        select_count = await all_selects.count()
        for i in range(select_count):
            loc = all_selects.nth(i)
            label = await loc.get_attribute('aria-label')
            if label and 'Algorithm' in label and 'Category' not in label:
                algo_select = loc
                break
    
    if not algo_select:
        raise Exception("Algorithm dropdown not found")
    
    await wait_for_stable(page, 1000)
    
    # Get current algorithm text to check if we need to change
    current_text = await algo_select.text_content()
    if not current_text or current_text.strip() == "":
        current_text = await algo_select.inner_text()
    
    if current_text and algorithm.lower() in current_text.lower():
        # Already selected
        print(f"    Algorithm already selected: {current_text.strip()}")
        return
    
    # Click to open dropdown
    await algo_select.click()
    await wait_for_stable(page, 1500)
    
    # Wait for dropdown list to appear (listbox or options)
    try:
        await page.wait_for_selector('[role="listbox"], [role="option"]', state='visible', timeout=5000)
    except:
        pass
    
    await wait_for_stable(page, 1000)
    
    # Find and click the option - make sure we're getting algorithm options, not category
    options = page.locator('[role="option"]')
    count = await options.count()
    
    if count == 0:
        await wait_for_stable(page, 2000)
        options = page.locator('[role="option"]')
        count = await options.count()
    
    # Filter out category options - algorithm options should NOT be in category list
    category_names = ["Basic Algorithms", "Server-Based (Combined)", "Precedence-Constrained", 
                     "Overload Handling", "Aperiodic Scheduling"]
    
    # Try exact match first
    for i in range(count):
        text = await options.nth(i).text_content()
        if not text:
            text = await options.nth(i).inner_text()
        if text:
            text = text.strip()
            # Skip if it's a category option
            if any(cat.lower() in text.lower() for cat in category_names):
                continue
            if algorithm == text or algorithm.lower() == text.lower():
                await options.nth(i).click()
                await wait_for_network_idle(page, 3000)
                await wait_for_stable(page, 1000)
                return
    
    # Try partial match (contains)
    for i in range(count):
        text = await options.nth(i).text_content()
        if not text:
            text = await options.nth(i).inner_text()
        if text:
            text = text.strip()
            # Skip if it's a category option
            if any(cat.lower() in text.lower() for cat in category_names):
                continue
            # Try matching key parts
            algo_key = algorithm.split()[0] if algorithm.split() else algorithm
            if algo_key.lower() in text.lower() or algorithm.lower() in text.lower():
                print(f"    [DEBUG] Matched '{algorithm}' to '{text}' (partial match)")
                await options.nth(i).click()
                await wait_for_network_idle(page, 3000)
                await wait_for_stable(page, 1000)
                return
    
    # Debug: print all available options (filtered)
    available = []
    for i in range(count):
        text = await options.nth(i).text_content()
        if not text:
            text = await options.nth(i).inner_text()
        if text:
            text = text.strip()
            # Only include non-category options
            if not any(cat.lower() in text.lower() for cat in category_names):
                available.append(text)
    print(f"    [DEBUG] Available algorithms: {available}")
    raise Exception(f"Algorithm '{algorithm}' not found. Available: {available}")


async def select_results_tab(page: Page, tab_name: str):
    """Select a tab in the results panel."""
    await ensure_no_modals(page)
    await wait_for_network_idle(page, 2000)
    
    # Find the last tablist (results panel)
    tablists = page.locator('[role="tablist"]')
    tablist_count = await tablists.count()
    if tablist_count == 0:
        return
    
    tablist = tablists.last
    tabs = tablist.locator(f'[role="tab"]:has-text("{tab_name}")')
    if await tabs.count() > 0:
        # Check if already selected
        tab = tabs.first
        is_selected = await tab.get_attribute('aria-selected')
        if is_selected == 'true':
            return
        
        await tab.click()
        # Wait for tab content to load
        await wait_for_network_idle(page, 3000)
        # Verify tab is selected
        await wait_for_stable(page, 1000)


async def load_preset(page: Page, preset_name: str, category: str = None):
    """Load a preset by name. Optionally specify category to switch to that tab first."""
    await ensure_no_modals(page)
    await wait_for_network_idle(page, 2000)
    
    # Click Presets button
    preset_button = page.locator('button:has-text("Presets")')
    if await preset_button.count() > 0:
        await preset_button.click()
        # Wait for dialog to open
        await wait_for_element_visible(page, '[role="dialog"]', 5000)
        await wait_for_stable(page, 1500)
    
    # If category is specified, switch to that tab first
    if category:
        # Find tabs in the dialog
        dialog_tabs = page.locator('[role="dialog"] [role="tab"]')
        tab_count = await dialog_tabs.count()
        for i in range(tab_count):
            tab = dialog_tabs.nth(i)
            text = await tab.text_content()
            if text and category.lower() in text.lower():
                await tab.click()
                await wait_for_stable(page, 1500)
                break
    
    # Find the preset card - try multiple strategies
    # Strategy 1: Find by strong tag with preset name (exact match)
    preset_cards = page.locator(f'strong:has-text("{preset_name}")')
    card_count = await preset_cards.count()
    
    # Strategy 2: If not found, try partial match in all strong tags
    card = None
    if card_count == 0:
        # Try finding by partial name match
        all_strongs = page.locator('strong')
        strong_count = await all_strongs.count()
        for i in range(strong_count):
            text = await all_strongs.nth(i).text_content()
            if text:
                text = text.strip()
                # Filter out non-preset items
                if text.startswith('Step ') or text == 'Run':
                    continue
                if preset_name.lower() in text.lower() or text.lower() in preset_name.lower():
                    card = all_strongs.nth(i)
                    print(f"    [DEBUG] Found preset '{text}' matching '{preset_name}'")
                    break
    elif card_count == 1:
        card = preset_cards.first
    else:
        # Multiple matches, find the best one
        for i in range(card_count):
            text = await preset_cards.nth(i).text_content()
            if text and preset_name.lower() in text.lower():
                card = preset_cards.nth(i)
                break
        if not card:
            card = preset_cards.first
    
    if card:
        print(f"    [DEBUG] Found preset card for '{preset_name}', looking for Load button...")
        
        # Use JavaScript to find and click the Load button in the same container as the preset card
        # This is more reliable than navigating DOM with locators
        clicked = await page.evaluate("""
            (presetName) => {
                // Find all strong tags with the preset name
                const strongTags = document.querySelectorAll('strong');
                for (let strong of strongTags) {
                    if (strong.textContent && strong.textContent.includes(presetName)) {
                        // Find the parent container (column)
                        let container = strong;
                        for (let i = 0; i < 5; i++) {
                            container = container.parentElement;
                            if (!container) break;
                            
                            // Look for Load button in this container
                            const buttons = container.querySelectorAll('button');
                            for (let btn of buttons) {
                                if (btn.textContent && btn.textContent.trim() === 'Load') {
                                    // Make sure this is NOT a tab button
                                    const role = btn.getAttribute('role');
                                    const isTab = role === 'tab' || btn.closest('[role="tablist"]');
                                    if (!isTab) {
                                        // Click the strong tag first (as per user feedback)
                                        strong.scrollIntoView({ behavior: 'smooth', block: 'center' });
                                        strong.click();
                                        
                                        // Small delay then click Load
                                        setTimeout(() => {
                                            btn.scrollIntoView({ behavior: 'smooth', block: 'center' });
                                            btn.click();
                                        }, 300);
                                        return true;
                                    }
                                }
                            }
                        }
                    }
                }
                return false;
            }
        """, preset_name)
        
        if not clicked:
            # Fallback: try using Playwright locators, but be very specific
            # Make sure we're NOT clicking tabs - only buttons with text "Load" that are NOT tabs
            dialog = page.locator('[role="dialog"]')
            # Find Load buttons that are NOT tabs
            all_load_buttons = dialog.locator('button:has-text("Load")')
            button_count = await all_load_buttons.count()
            
            # Find the one in the same container as our preset card
            card_text = await card.text_content()
            for i in range(button_count):
                btn = all_load_buttons.nth(i)
                # Check if button is a tab
                role = await btn.get_attribute('role')
                if role == 'tab':
                    continue
                
                # Check if button is near our card
                # Get button's container and check if it contains our card text
                btn_container = btn.locator('..').locator('..').locator('..')
                container_text = await btn_container.text_content()
                if container_text and preset_name.lower() in container_text.lower():
                    print(f"    [DEBUG] Found Load button using Playwright fallback")
                    await card.click()
                    await wait_for_stable(page, 500)
                    await btn.click()
                    clicked = True
                    break
        
        if not clicked:
            raise Exception(f"Could not find or click Load button for preset '{preset_name}'")
        
        # Wait for dialog to close (it closes automatically after Load)
        print(f"    [DEBUG] Waiting for dialog to close...")
        try:
            await page.wait_for_selector('[role="dialog"]', state='hidden', timeout=8000)
            print(f"    [DEBUG] Dialog closed")
        except:
            print(f"    [WARNING] Dialog did not close within timeout")
        
        # Wait for Streamlit to rerun and process the preset
        # This is critical - Streamlit needs to rerun to apply the preset
        print(f"    [DEBUG] Waiting for Streamlit rerun...")
        await wait_for_network_idle(page, 8000)
        
        # Wait for the page to update
        await wait_for_stable(page, 3000)
        
        # Verify preset was loaded by checking task count in the task grid
        print(f"    [DEBUG] Verifying preset was loaded...")
        await wait_for_stable(page, 2000)
        
        # Check task grid - count rows that contain task data
        task_selectors = [
            'table tbody tr',
            '[data-testid*="stDataFrame"] tbody tr',
            '.stDataFrame tbody tr',
            '[role="table"] tbody tr',
            '[role="rowgroup"] [role="row"]'
        ]
        
        row_count = 0
        for selector in task_selectors:
            rows = page.locator(selector)
            count = await rows.count()
            if count > 0:
                row_count = count
                # Filter out header rows
                if row_count > 0:
                    first_row_text = await rows.nth(0).text_content()
                    if first_row_text and ('ID' in first_row_text or 'id' in first_row_text.lower()):
                        row_count = max(0, count - 1)  # Subtract header row
                break
        
        print(f"    [DEBUG] Found {row_count} task row(s) in grid")
        
        # If we still only have 1 task, wait longer and try again
        if row_count <= 1:
            print(f"    [WARNING] Only {row_count} task(s) found, waiting longer for preset to load...")
            await wait_for_network_idle(page, 6000)
            await wait_for_stable(page, 3000)
            # Re-check
            for selector in task_selectors:
                rows = page.locator(selector)
                count = await rows.count()
                if count > 0:
                    row_count = count
                    first_row_text = await rows.nth(0).text_content()
                    if first_row_text and ('ID' in first_row_text or 'id' in first_row_text.lower()):
                        row_count = max(0, count - 1)
                    break
            print(f"    [DEBUG] After additional wait: {row_count} task row(s)")
        
        if row_count <= 1:
            print(f"    [ERROR] Preset may not have loaded correctly - only {row_count} task(s) found")
            print(f"    [INFO] Expected multiple tasks from preset '{preset_name}'")
        
        await ensure_no_modals(page)
        await wait_for_stable(page, 2000)
        return
    
    # Debug: print available presets
    all_strongs = page.locator('strong')
    available = []
    strong_count = await all_strongs.count()
    for i in range(min(strong_count, 20)):  # Limit to first 20
        text = await all_strongs.nth(i).text_content()
        if text:
            available.append(text.strip())
    raise Exception(f"Preset '{preset_name}' not found. Available presets (first 20): {available}")


async def run_simulation(page: Page):
    """Click Run button and wait for simulation to complete."""
    await ensure_no_modals(page)
    await wait_for_network_idle(page, 2000)
    
    run_button = page.locator('button:has-text("Run")')
    if await run_button.count() > 0:
        await run_button.click()
        # Wait for "Running..." indicator to appear
        try:
            await page.wait_for_selector('text=Running...', timeout=2000)
        except:
            pass
        
        # Wait for "Running..." to disappear (simulation complete)
        try:
            await page.wait_for_selector('text=Running...', state='hidden', timeout=10000)
        except:
            pass
        
        # Wait for network to be idle and UI to stabilize
        await wait_for_network_idle(page, 5000)
        await ensure_no_modals(page)
        await wait_for_stable(page, 2000)


async def expand_advanced_options(page: Page):
    """Expand Advanced Options section."""
    await ensure_no_modals(page)
    await wait_for_network_idle(page, 2000)
    
    # Look for the expander
    expanders = page.locator('text=Advanced Options')
    if await expanders.count() > 0:
        expander = expanders.first.locator('..').locator('..')
        # Check if already expanded (has keyboard_arrow_down)
        arrow_down = expander.locator('text=keyboard_arrow_down')
        if await arrow_down.count() == 0:
            await expander.click()
            # Wait for Advanced Options to expand
            await wait_for_element_visible(page, '[role="tablist"]', 3000)
            await wait_for_stable(page, 800)


async def select_advanced_tab(page: Page, tab_name: str):
    """Select a tab in Advanced Options."""
    await expand_advanced_options(page)
    await ensure_no_modals(page)
    await wait_for_network_idle(page, 2000)
    
    # Find tabs in Advanced Options - they should be in a tablist within Advanced Options
    # Advanced Options has its own tablist, separate from the results panel
    advanced_tablist = page.locator('text=Advanced Options').locator('..').locator('..').locator('[role="tablist"]')
    
    # If we can't find it that way, try finding all tablists and get the one in Advanced Options
    all_tablists = page.locator('[role="tablist"]')
    tablist_count = await all_tablists.count()
    
    target_tab = None
    for i in range(tablist_count):
        tablist = all_tablists.nth(i)
        tabs = tablist.locator(f'[role="tab"]:has-text("{tab_name}")')
        if await tabs.count() > 0:
            # Check if this tablist is in Advanced Options area
            # Advanced Options tablist should be after the "Advanced Options" text
            tab = tabs.first
            # Try to verify it's in Advanced Options by checking parent
            parent_text = await tab.locator('..').locator('..').locator('..').text_content()
            if parent_text and 'Advanced Options' in parent_text:
                target_tab = tab
                break
            # If we can't verify, use the last matching tab (Advanced Options is usually last)
            if not target_tab:
                target_tab = tabs.last
    
    if target_tab:
        # Check if already selected
        is_selected = await target_tab.get_attribute('aria-selected')
        if is_selected == 'true':
            return
        
        # Make sure tab is visible before clicking
        await wait_for_element_visible(page, f'[role="tab"]:has-text("{tab_name}")', 5000)
        
        # Use JavaScript to click if Playwright click fails
        try:
            await target_tab.click(timeout=5000)
        except:
            # Fallback: use JavaScript
            await page.evaluate(f"""
                (tabName) => {{
                    const tabs = document.querySelectorAll('[role="tab"]');
                    for (let tab of tabs) {{
                        if (tab.textContent && tab.textContent.includes(tabName)) {{
                            // Check if it's in Advanced Options
                            let parent = tab.closest('[role="tablist"]');
                            if (parent) {{
                                let container = parent.closest('div');
                                if (container && container.textContent && container.textContent.includes('Advanced Options')) {{
                                    tab.click();
                                    return true;
                                }}
                            }}
                        }}
                    }}
                    return false;
                }}
            """, tab_name)
        
        # Wait for tab content to load
        await wait_for_network_idle(page, 2000)
        await wait_for_stable(page, 1000)
    else:
        raise Exception(f"Advanced Options tab '{tab_name}' not found")


async def take_screenshot(page: Page, filename: str, subdirectory: str = ""):
    """Take a screenshot and save it."""
    await ensure_no_modals(page)
    
    if subdirectory:
        target_dir = SCREENSHOTS_DIR / subdirectory
        target_dir.mkdir(parents=True, exist_ok=True)
        filepath = target_dir / filename
    else:
        SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
        filepath = SCREENSHOTS_DIR / filename
    
    # Check if file exists
    exists = filepath.exists()
    
    try:
        await page.screenshot(path=str(filepath), full_page=True)
        STATS["total"] += 1
        if exists:
            STATS["replaced"] += 1
            print(f"  [REPLACED] {filepath.name}")
        else:
            STATS["new"] += 1
            print(f"  [NEW] {filepath.name}")
        return True
    except Exception as e:
        STATS["errors"] += 1
        print(f"  [ERROR] Error capturing {filename}: {e}")
        return False


async def capture_part1_getting_started(page: Page):
    """Capture Part 1: Getting Started screenshots."""
    print("\n=== Part 1: Getting Started ===")
    await page.goto(BASE_URL)
    await wait_for_network_idle(page, 5000)
    await ensure_no_modals(page)
    await wait_for_stable(page, 2000)
    
    await take_screenshot(page, "part1-01-initial-state.png", "part1-getting-started")
    await take_screenshot(page, "part1-02-full-layout.png", "part1-getting-started")
    await take_screenshot(page, "part1-03-header-section.png", "part1-getting-started")
    await take_screenshot(page, "part1-04-configuration-panel.png", "part1-getting-started")
    await take_screenshot(page, "part1-05-results-panel-empty.png", "part1-getting-started")


async def capture_part2_basic_algorithms(page: Page):
    """Capture Part 2: Basic Algorithms screenshots."""
    print("\n=== Part 2: Basic Algorithms ===")
    
    # RMS
    print("  RMS...")
    await select_category(page, "Basic Algorithms")
    # Wait extra time for algorithm dropdown to update after category change
    await wait_for_network_idle(page, 3000)
    await wait_for_stable(page, 2000)
    await select_algorithm(page, "RMS (Rate Monotonic)")
    await ensure_no_modals(page)
    await take_screenshot(page, "part2-rms-01-algorithm-selection.png", "part2-basic-algorithms")
    
    # Task configuration screenshot
    await take_screenshot(page, "part2-rms-02-task-configuration.png", "part2-basic-algorithms")
    
    await run_simulation(page)
    # Results metrics
    await take_screenshot(page, "part2-rms-03-results-metrics.png", "part2-basic-algorithms")
    
    await select_results_tab(page, "Gantt")
    await take_screenshot(page, "part2-rms-04-gantt-chart.png", "part2-basic-algorithms")
    
    await select_results_tab(page, "Metrics")
    await take_screenshot(page, "part2-rms-05-metrics-dashboard.png", "part2-basic-algorithms")
    
    await select_results_tab(page, "Timeline")
    await take_screenshot(page, "part2-rms-06-timeline-viewer.png", "part2-basic-algorithms")
    
    await select_results_tab(page, "Analysis")
    await take_screenshot(page, "part2-rms-07-analysis-tab.png", "part2-basic-algorithms")
    
    await select_results_tab(page, "Export")
    await take_screenshot(page, "part2-rms-08-export-tab.png", "part2-basic-algorithms")
    
    # EDF
    print("  EDF...")
    await select_algorithm(page, "EDF (Earliest Deadline First)")
    await ensure_no_modals(page)
    await take_screenshot(page, "part2-edf-01-algorithm-selection.png", "part2-basic-algorithms")
    
    await take_screenshot(page, "part2-edf-02-task-configuration.png", "part2-basic-algorithms")
    
    await run_simulation(page)
    await select_results_tab(page, "Gantt")
    await take_screenshot(page, "part2-edf-03-gantt-chart.png", "part2-basic-algorithms")
    
    await select_results_tab(page, "Timeline")
    await take_screenshot(page, "part2-edf-04-priority-timeline.png", "part2-basic-algorithms")
    
    await select_results_tab(page, "Analysis")
    await take_screenshot(page, "part2-edf-05-analysis.png", "part2-basic-algorithms")
    
    # DMS
    print("  DMS...")
    await select_algorithm(page, "DMS (Deadline Monotonic)")
    await ensure_no_modals(page)
    await take_screenshot(page, "part2-dms-01-algorithm-selection.png", "part2-basic-algorithms")
    
    await take_screenshot(page, "part2-dms-02-task-configuration.png", "part2-basic-algorithms")
    
    await run_simulation(page)
    await select_results_tab(page, "Timeline")
    await take_screenshot(page, "part2-dms-03-priority-timeline.png", "part2-basic-algorithms")
    
    # LLF
    print("  LLF...")
    await select_algorithm(page, "LLF (Least Laxity First)")
    await ensure_no_modals(page)
    await take_screenshot(page, "part2-llf-01-algorithm-selection.png", "part2-basic-algorithms")
    
    await run_simulation(page)
    await select_results_tab(page, "Timeline")
    await take_screenshot(page, "part2-llf-02-laxity-timeline.png", "part2-basic-algorithms")


async def capture_part3_server_algorithms(page: Page):
    """Capture Part 3: Server Algorithms screenshots."""
    print("\n=== Part 3: Server Algorithms ===")
    
    await select_category(page, "Server-Based (Combined)")
    await ensure_no_modals(page)
    await take_screenshot(page, "part3-server-01-category-selection.png", "part3-server-algorithms")
    
    # Polling Server
    print("  Polling Server...")
    await load_preset(page, "Basic Polling Server", "Server-Based (Combined)")
    await ensure_no_modals(page)
    await take_screenshot(page, "part3-polling-04-algorithm-selection.png", "part3-server-algorithms")
    
    # Server configuration
    await take_screenshot(page, "part3-server-02-server-configuration.png", "part3-server-algorithms")
    
    # Task grid with periodic and aperiodic
    await take_screenshot(page, "part3-polling-05-task-grid-with-periodic-aperiodic.png", "part3-server-algorithms")
    
    await run_simulation(page)
    await select_results_tab(page, "Gantt")
    await take_screenshot(page, "part3-polling-02-gantt-chart.png", "part3-server-algorithms")
    
    await select_results_tab(page, "Analysis")
    await take_screenshot(page, "part3-polling-03-server-analysis.png", "part3-server-algorithms")
    await take_screenshot(page, "part3-polling-06-response-times-table.png", "part3-server-algorithms")
    
    # Deferrable Server
    print("  Deferrable Server...")
    await load_preset(page, "Deferrable Server", "Server-Based (Combined)")
    await run_simulation(page)
    await select_results_tab(page, "Gantt")
    await take_screenshot(page, "part3-deferrable-01-gantt.png", "part3-server-algorithms")
    
    # Sporadic Server
    print("  Sporadic Server...")
    await load_preset(page, "Sporadic Server", "Server-Based (Combined)")
    await run_simulation(page)
    await select_results_tab(page, "Gantt")
    await take_screenshot(page, "part3-sporadic-01-gantt.png", "part3-server-algorithms")
    
    # Background Scheduler
    print("  Background Scheduler...")
    await load_preset(page, "Background Scheduler (Baseline)", "Server-Based (Combined)")
    await run_simulation(page)
    await select_results_tab(page, "Gantt")
    await take_screenshot(page, "part3-background-01-gantt.png", "part3-server-algorithms")


async def capture_part4_precedence(page: Page):
    """Capture Part 4: Precedence-Constrained screenshots."""
    print("\n=== Part 4: Precedence-Constrained ===")
    
    # Open preset dialog
    preset_button = page.locator('button:has-text("Presets")')
    await preset_button.click()
    await wait_for_stable(page, 1000)
    await take_screenshot(page, "part4-precedence-constrained-01-preset-dialog.png", "part4-precedence")
    
    # Load RMS Chain preset
    await load_preset(page, "Chain Dependencies", "Precedence-Constrained")
    await ensure_no_modals(page)
    await take_screenshot(page, "part4-precedence-constrained-02-rms-chain-config.png", "part4-precedence")
    
    # Expand Advanced Options and show Precedence tab
    await expand_advanced_options(page)
    await select_advanced_tab(page, "Precedence")
    await take_screenshot(page, "part4-precedence-constrained-03-rms-chain-precedence-tab.png", "part4-precedence")
    
    await run_simulation(page)
    await select_results_tab(page, "Gantt")
    await take_screenshot(page, "part4-precedence-constrained-04-rms-chain-gantt.png", "part4-precedence")
    
    await select_results_tab(page, "Timeline")
    await take_screenshot(page, "part4-precedence-constrained-05-rms-chain-precedence-graph.png", "part4-precedence")
    
    await select_results_tab(page, "Analysis")
    await take_screenshot(page, "part4-precedence-constrained-06-rms-chain-analysis.png", "part4-precedence")
    
    # EDF Fork Pattern
    print("  EDF Fork Pattern...")
    await load_preset(page, "Fork Pattern", "Precedence-Constrained")
    await ensure_no_modals(page)
    await take_screenshot(page, "part4-precedence-constrained-07-edf-fork-config.png", "part4-precedence")
    
    await run_simulation(page)
    await select_results_tab(page, "Gantt")
    await take_screenshot(page, "part4-precedence-constrained-08-edf-fork-gantt.png", "part4-precedence")
    
    await select_results_tab(page, "Timeline")
    await take_screenshot(page, "part4-precedence-constrained-09-edf-fork-precedence-graph.png", "part4-precedence")
    
    await select_results_tab(page, "Analysis")
    await take_screenshot(page, "part4-precedence-constrained-11-edf-fork-analysis.png", "part4-precedence")
    
    # DMS Diamond Pattern
    print("  DMS Diamond Pattern...")
    await load_preset(page, "Diamond Pattern", "Precedence-Constrained")
    await ensure_no_modals(page)
    await take_screenshot(page, "part4-precedence-constrained-10-dms-diamond-config.png", "part4-precedence")
    
    await expand_advanced_options(page)
    await select_advanced_tab(page, "Precedence")
    await take_screenshot(page, "part4-precedence-constrained-11-dms-diamond-precedence-tab.png", "part4-precedence")
    
    await run_simulation(page)
    await select_results_tab(page, "Gantt")
    await take_screenshot(page, "part4-precedence-constrained-12-dms-diamond-gantt.png", "part4-precedence")
    
    await select_results_tab(page, "Timeline")
    await take_screenshot(page, "part4-precedence-constrained-13-dms-diamond-precedence-graph.png", "part4-precedence")
    
    await select_results_tab(page, "Analysis")
    await take_screenshot(page, "part4-precedence-constrained-14-dms-diamond-analysis.png", "part4-precedence")


async def capture_part5_aperiodic(page: Page):
    """Capture Part 5: Aperiodic Scheduling screenshots."""
    print("\n=== Part 5: Aperiodic Scheduling ===")
    
    # Open preset dialog
    preset_button = page.locator('button:has-text("Presets")')
    await preset_button.click()
    await wait_for_stable(page, 1000)
    await take_screenshot(page, "part5-aperiodic-01-preset-dialog.png", "part5-aperiodic")
    
    await select_category(page, "Aperiodic Scheduling")
    
    # EDF+HVDF Value Max
    await load_preset(page, "Value Maximization", "Aperiodic Scheduling")
    await ensure_no_modals(page)
    await take_screenshot(page, "part5-aperiodic-02-edf-hvdf-value-max-config.png", "part5-aperiodic")
    
    await run_simulation(page)
    await select_results_tab(page, "Gantt")
    await take_screenshot(page, "part5-aperiodic-03-edf-hvdf-value-max-gantt.png", "part5-aperiodic")
    
    await select_results_tab(page, "Metrics")
    await take_screenshot(page, "part5-aperiodic-04-edf-hvdf-value-max-metrics.png", "part5-aperiodic")
    
    await select_results_tab(page, "Analysis")
    await take_screenshot(page, "part5-aperiodic-05-edf-hvdf-value-max-analysis.png", "part5-aperiodic")
    
    # EDF+HVDF Staggered
    print("  EDF+HVDF Staggered...")
    await load_preset(page, "Staggered Arrivals", "Aperiodic Scheduling")
    await ensure_no_modals(page)
    await take_screenshot(page, "part5-aperiodic-06-edf-hvdf-staggered-config.png", "part5-aperiodic")
    
    await run_simulation(page)
    await select_results_tab(page, "Gantt")
    await take_screenshot(page, "part5-aperiodic-07-edf-hvdf-staggered-gantt.png", "part5-aperiodic")
    
    await select_results_tab(page, "Analysis")
    await take_screenshot(page, "part5-aperiodic-08-edf-hvdf-staggered-analysis.png", "part5-aperiodic")
    
    # EDF+HVDF Burst
    print("  EDF+HVDF Burst...")
    await load_preset(page, "Burst Arrivals", "Aperiodic Scheduling")
    await ensure_no_modals(page)
    await take_screenshot(page, "part5-aperiodic-09-edf-hvdf-burst-config.png", "part5-aperiodic")
    
    await run_simulation(page)
    await select_results_tab(page, "Gantt")
    await take_screenshot(page, "part5-aperiodic-10-edf-hvdf-burst-gantt.png", "part5-aperiodic")
    
    await select_results_tab(page, "Analysis")
    await take_screenshot(page, "part5-aperiodic-11-edf-hvdf-burst-analysis.png", "part5-aperiodic")
    
    # HVDF Only
    print("  HVDF Only...")
    await select_algorithm(page, "HVDF Only")
    await ensure_no_modals(page)
    await take_screenshot(page, "part5-aperiodic-12-hvdf-only-config.png", "part5-aperiodic")
    
    await run_simulation(page)
    await select_results_tab(page, "Gantt")
    await take_screenshot(page, "part5-aperiodic-13-hvdf-only-gantt.png", "part5-aperiodic")
    
    await select_results_tab(page, "Analysis")
    await take_screenshot(page, "part5-aperiodic-14-hvdf-only-analysis.png", "part5-aperiodic")


async def capture_part6_overload(page: Page):
    """Capture Part 6: Overload Handling screenshots."""
    print("\n=== Part 6: Overload Handling ===")
    
    await select_category(page, "Overload Handling")
    
    # FC-EDF
    print("  FC-EDF...")
    await select_algorithm(page, "FC-EDF (Feedback Control)")
    await ensure_no_modals(page)
    await take_screenshot(page, "part6-overload-01-fc-edf-config.png", "part6-overload")
    
    await expand_advanced_options(page)
    await select_advanced_tab(page, "Overload")
    await ensure_no_modals(page)
    await take_screenshot(page, "part6-overload-02-fc-edf-overload-tab.png", "part6-overload")
    
    await run_simulation(page)
    await select_results_tab(page, "Gantt")
    await take_screenshot(page, "part6-overload-03-fc-edf-gantt.png", "part6-overload")
    
    await select_results_tab(page, "Metrics")
    await take_screenshot(page, "part6-overload-04-fc-edf-service-level-plot.png", "part6-overload")
    
    await select_results_tab(page, "Analysis")
    await take_screenshot(page, "part6-overload-05-fc-edf-analysis.png", "part6-overload")
    
    # Feedback (m,k)-RMS
    print("  Feedback (m,k)-RMS...")
    await select_algorithm(page, "Feedback (m,k)-RMS")
    await ensure_no_modals(page)
    await take_screenshot(page, "part6-overload-06-mk-rms-config.png", "part6-overload")
    
    await expand_advanced_options(page)
    await select_advanced_tab(page, "Overload")
    await take_screenshot(page, "part6-overload-07-mk-rms-overload-tab.png", "part6-overload")
    
    await take_screenshot(page, "part6-overload-09-mk-rms-task-grid.png", "part6-overload")
    
    await run_simulation(page)
    await select_results_tab(page, "Metrics")
    await take_screenshot(page, "part6-overload-08-mk-rms-mk-history.png", "part6-overload")
    
    await select_results_tab(page, "Gantt")
    await take_screenshot(page, "part6-overload-10-mk-rms-gantt.png", "part6-overload")
    
    # Imprecise Computation
    print("  Imprecise Computation...")
    await select_algorithm(page, "Imprecise Computation")
    await ensure_no_modals(page)
    await take_screenshot(page, "part6-overload-11-imprecise-algorithm-selection.png", "part6-overload")
    
    await take_screenshot(page, "part6-overload-12-imprecise-task-grid.png", "part6-overload")
    
    await run_simulation(page)
    await select_results_tab(page, "Gantt")
    await take_screenshot(page, "part6-overload-13-imprecise-gantt.png", "part6-overload")
    
    # HVDF (Value-Based) - Overload
    print("  HVDF (Value-Based) - Overload...")
    await select_algorithm(page, "HVDF (Value-Based)")
    await ensure_no_modals(page)
    await take_screenshot(page, "part6-overload-14-hvdf-algorithm-selection.png", "part6-overload")
    
    await take_screenshot(page, "part6-overload-15-hvdf-task-grid-with-values.png", "part6-overload")
    
    await run_simulation(page)
    await select_results_tab(page, "Gantt")
    await take_screenshot(page, "part6-overload-16-hvdf-gantt.png", "part6-overload")
    
    await select_results_tab(page, "Analysis")
    await take_screenshot(page, "part6-overload-17-hvdf-analysis.png", "part6-overload")
    
    # (m,k)-Firm Tasks
    print("  (m,k)-Firm Tasks...")
    await select_algorithm(page, "(m,k)-Firm Tasks")
    await ensure_no_modals(page)
    await take_screenshot(page, "part6-overload-18-mk-firm-algorithm-selection.png", "part6-overload")
    
    await take_screenshot(page, "part6-overload-19-mk-firm-task-grid-with-mk-column.png", "part6-overload")
    
    await run_simulation(page)
    await select_results_tab(page, "Metrics")
    await take_screenshot(page, "part6-overload-20-mk-firm-mk-history-chart.png", "part6-overload")
    
    await select_results_tab(page, "Analysis")
    await take_screenshot(page, "part6-overload-21-mk-firm-analysis.png", "part6-overload")


async def capture_part7_resource_sharing(page: Page):
    """Capture Part 7: Resource Sharing screenshots."""
    print("\n=== Part 7: Resource Sharing ===")
    
    await select_category(page, "Basic Algorithms")
    await select_algorithm(page, "RMS (Rate Monotonic)")
    await expand_advanced_options(page)
    await select_advanced_tab(page, "Resources")
    await ensure_no_modals(page)
    await take_screenshot(page, "part7-resource-01-resources-tab.png", "part7-advanced")
    
    # Enable resource sharing - find checkbox near the label
    checkbox_label = page.locator('text=Enable Resource Sharing')
    if await checkbox_label.count() > 0:
        # Find the checkbox in the same container
        container = checkbox_label.locator('..').locator('..')
        checkbox = container.locator('input[type="checkbox"]')
        if await checkbox.count() == 0:
            # Try different container level
            checkbox = checkbox_label.locator('..').locator('input[type="checkbox"]')
        if await checkbox.count() > 0:
            await checkbox.click()
            await wait_for_stable(page, 1000)
    
    await ensure_no_modals(page)
    await take_screenshot(page, "part7-resource-02-enable-resource-sharing-checked.png", "part7-advanced")
    
    # Protocol selection PIP
    await take_screenshot(page, "part7-resource-03-protocol-selection-pip.png", "part7-advanced")
    
    # Resource grid
    await take_screenshot(page, "part7-resource-04-resource-grid.png", "part7-advanced")
    
    # Task grid with Resources and CS columns
    await take_screenshot(page, "part7-resource-05-task-grid-with-resources-cs.png", "part7-advanced")
    
    await run_simulation(page)
    await select_results_tab(page, "Gantt")
    await take_screenshot(page, "part7-resource-06-gantt-with-blocking.png", "part7-advanced")
    
    await select_results_tab(page, "Analysis")
    await take_screenshot(page, "part7-resource-07-analysis-blocking-time.png", "part7-advanced")
    
    # Switch to PCP protocol - need to go back to Resources tab
    await expand_advanced_options(page)
    await select_advanced_tab(page, "Resources")
    await ensure_no_modals(page)
    await wait_for_stable(page, 1000)
    
    # Find protocol selector
    protocol_selectors = [
        '[aria-label*="Protocol"]',
        'selectbox:has-text("Protocol")',
    ]
    
    protocol_select = None
    for selector in protocol_selectors:
        locators = page.locator(selector)
        count = await locators.count()
        if count > 0:
            # Get the one in Advanced Options (not in main config)
            for i in range(count):
                loc = locators.nth(i)
                # Check if it's in Advanced Options area
                parent_text = await loc.locator('..').locator('..').locator('..').text_content()
                if parent_text and 'Advanced Options' in parent_text:
                    protocol_select = loc
                    break
            if protocol_select:
                break
    
    if protocol_select:
        await protocol_select.click()
        await wait_for_stable(page, 800)
        options = page.locator('[role="option"]')
        count = await options.count()
        for i in range(count):
            text = await options.nth(i).text_content()
            if text and "Priority Ceiling" in text:
                await options.nth(i).click()
                await wait_for_network_idle(page, 3000)
                await wait_for_stable(page, 1000)
                break
        
        await take_screenshot(page, "part7-resource-08-protocol-selection-pcp.png", "part7-advanced")
    else:
        print("    [WARNING] Could not find Protocol selector for PCP screenshot")


async def main():
    """Main capture function."""
    print("=" * 70)
    print("Comprehensive Screenshot Capture for Real-Time Scheduling Simulator")
    print("=" * 70)
    print(f"\nTarget URL: {BASE_URL}")
    print(f"Screenshots directory: {SCREENSHOTS_DIR}")
    
    # Check if Streamlit app is running
    print("\nChecking if Streamlit app is running...")
    port_open = check_port_open("localhost", 8501)
    url_accessible = check_url_accessible(BASE_URL)
    
    if port_open and url_accessible:
        print(f"  [OK] Streamlit app is running on {BASE_URL}")
        skip_prompt = True
    else:
        print(f"  [WARNING] Streamlit app is not accessible at {BASE_URL}")
        print("  Make sure Streamlit app is running on http://localhost:8501")
        skip_prompt = False
    
    # Check if Playwright browsers are installed
    try:
        async with async_playwright() as p:
            # Try to launch browser to check if it's installed
            browser = await p.chromium.launch(headless=False)
            await browser.close()
    except Exception as e:
        if "Executable doesn't exist" in str(e) or "chromium" in str(e).lower():
            print("\n" + "=" * 70)
            print("ERROR: Playwright browsers are not installed!")
            print("=" * 70)
            print("\nPlease run the following command to install browsers:")
            print("  python -m playwright install chromium")
            print("\nOr install all browsers:")
            print("  python -m playwright install")
            print("=" * 70)
            return
        else:
            raise
    
    if not skip_prompt:
        print("\nPress Enter to start (or Ctrl+C to cancel)...")
        try:
            input()
        except EOFError:
            # Running non-interactively, continue anyway
            print("  (Non-interactive mode, continuing...)")
    else:
        print("\nStarting automatically in 2 seconds...")
        await asyncio.sleep(2)
    
    # Parse command line arguments for resume functionality
    parser = argparse.ArgumentParser(description='Capture screenshots for Real-Time Scheduling Simulator')
    parser.add_argument('--start-from', type=int, help='Start from part number (1-7). Example: --start-from 3')
    parser.add_argument('--part', type=int, help='Run only specific part (1-7). Example: --part 2')
    args = parser.parse_args()
    
    # Determine which parts to run
    start_part = 1
    end_part = 7
    
    if args.start_from:
        start_part = args.start_from
        end_part = 7
    elif args.part:
        start_part = args.part
        end_part = args.part
    else:
        # Interactive mode: ask user if they want to resume
        print("\n" + "=" * 70)
        print("Resume Options:")
        print("  Press Enter to start from beginning")
        print("  Or enter part number (1-7) to start from that part")
        print("  Available parts:")
        for part_num, (part_name, _) in PARTS.items():
            print(f"    {part_num}: {part_name}")
        print("=" * 70)
        
        try:
            user_input = input("\nStart from part (or Enter for beginning): ").strip()
            if user_input:
                start_part = int(user_input)
                end_part = 7  # Run to the end
            else:
                start_part = 1
                end_part = 7
        except (ValueError, EOFError, KeyboardInterrupt):
            print("\nStarting from beginning...")
            start_part = 1
            end_part = 7
    
    # Validate part numbers
    if start_part < 1 or start_part > 7:
        print(f"[ERROR] Invalid part number: {start_part}. Must be 1-7")
        return
    if end_part < 1 or end_part > 7:
        print(f"[ERROR] Invalid end part number: {end_part}. Must be 1-7")
        return
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = await context.new_page()
        
        try:
            # Navigate to page first
            await page.goto(BASE_URL)
            await wait_for_network_idle(page, 5000)
            await ensure_no_modals(page)
            await wait_for_stable(page, 2000)
            
            # Map of part numbers to capture functions
            capture_functions = {
                1: capture_part1_getting_started,
                2: capture_part2_basic_algorithms,
                3: capture_part3_server_algorithms,
                4: capture_part4_precedence,
                5: capture_part5_aperiodic,
                6: capture_part6_overload,
                7: capture_part7_resource_sharing,
            }
            
            # Run the specified parts
            for part_num in range(start_part, end_part + 1):
                if part_num in capture_functions:
                    part_name, _ = PARTS[part_num]
                    print(f"\n{'=' * 70}")
                    print(f"Running {part_name} (Part {part_num}/{end_part})")
                    print(f"{'=' * 70}")
                    try:
                        await capture_functions[part_num](page)
                        print(f"\n[OK] Completed {part_name}")
                    except Exception as e:
                        print(f"\n[ERROR] Error in {part_name}: {e}")
                        import traceback
                        traceback.print_exc()
                        print(f"\n{'=' * 70}")
                        print(f"[INFO] To resume from this part, run:")
                        print(f"  python capture_all_screenshots.py --start-from {part_num}")
                        print(f"{'=' * 70}")
                        
                        # Ask if user wants to continue
                        if hasattr(args, 'continue_on_error') and args.continue_on_error:
                            print(f"[INFO] --continue-on-error flag set, continuing to next part...")
                            continue
                        elif args.start_from or args.part:
                            # Non-interactive mode with specific part, don't continue
                            print(f"[INFO] Stopping execution. Fix the error and resume with --start-from {part_num}")
                            break
                        else:
                            # Interactive mode: ask user
                            try:
                                continue_choice = input("\nContinue to next part? (y/n): ").strip().lower()
                                if continue_choice != 'y':
                                    print(f"\n[INFO] Stopped. Resume with: --start-from {part_num + 1}")
                                    break
                            except (EOFError, KeyboardInterrupt):
                                print(f"\n[INFO] Interrupted. Resume with: --start-from {part_num + 1}")
                                break
                else:
                    print(f"[WARNING] Part {part_num} not found in capture_functions")
            
        except Exception as e:
            print(f"\n[ERROR] Error during capture: {e}")
            import traceback
            traceback.print_exc()
        finally:
            await browser.close()
        
        # Print statistics
        print("\n" + "=" * 70)
        print("Capture Statistics:")
        print(f"  Total screenshots: {STATS['total']}")
        print(f"  New files: {STATS['new']}")
        print(f"  Replaced files: {STATS['replaced']}")
        print(f"  Errors: {STATS['errors']}")
        print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())

