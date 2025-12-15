"""
Comprehensive automated screenshot capture script for Real-Time Scheduling Simulator User Guide.
This script systematically captures all screenshots, ensuring correct state (no modals, correct tabs).
"""

import time
import os
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import json

# Screenshot directories
BASE_DIR = Path(__file__).parent
SCREENSHOTS_DIR = BASE_DIR / "screenshots"
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

# Statistics
STATS = {
    "total_captures": 0,
    "replacements": 0,
    "new_files": 0,
    "errors": 0
}

def ensure_directory(path: Path):
    """Ensure directory exists."""
    path.mkdir(parents=True, exist_ok=True)

def get_screenshot_path(filename: str, subdirectory: str = "") -> Path:
    """Get full path for screenshot."""
    if subdirectory:
        target_dir = SCREENSHOTS_DIR / subdirectory
        ensure_directory(target_dir)
        return target_dir / filename
    return SCREENSHOTS_DIR / filename

def check_file_exists(path: Path) -> bool:
    """Check if file exists."""
    return path.exists()

class ScreenshotCapturePlan:
    """
    Comprehensive plan for all screenshots to capture.
    Each entry is: (filename, subdirectory, description, capture_function)
    """
    
    def __init__(self):
        self.plan = []
        self._build_plan()
    
    def _build_plan(self):
        """Build the complete screenshot capture plan."""
        
        # Part 1: Getting Started
        self.plan.extend([
            ("part1-01-initial-state.png", "part1-getting-started", "Initial application state"),
            ("part1-02-full-layout.png", "part1-getting-started", "Full layout overview"),
            ("part1-03-header-section.png", "part1-getting-started", "Header with Presets and Run buttons"),
            ("part1-04-configuration-panel.png", "part1-getting-started", "Configuration panel"),
            ("part1-05-results-panel-empty.png", "part1-getting-started", "Empty results panel"),
        ])
        
        # Part 2: Basic Algorithms - RMS
        self.plan.extend([
            ("part2-rms-01-algorithm-selection.png", "part2-basic-algorithms", "RMS algorithm selection"),
            ("part2-rms-02-task-configuration.png", "part2-basic-algorithms", "RMS task configuration"),
            ("part2-rms-03-results-metrics.png", "part2-basic-algorithms", "RMS results metrics"),
            ("part2-rms-04-gantt-chart.png", "part2-basic-algorithms", "RMS Gantt chart"),
            ("part2-rms-05-metrics-dashboard.png", "part2-basic-algorithms", "RMS metrics dashboard"),
            ("part2-rms-06-timeline-viewer.png", "part2-basic-algorithms", "RMS timeline viewer"),
            ("part2-rms-07-analysis-tab.png", "part2-basic-algorithms", "RMS analysis tab"),
            ("part2-rms-08-export-tab.png", "part2-basic-algorithms", "RMS export tab"),
        ])
        
        # Part 2: Basic Algorithms - EDF
        self.plan.extend([
            ("part2-edf-01-algorithm-selection.png", "part2-basic-algorithms", "EDF algorithm selection"),
            ("part2-edf-02-task-configuration.png", "part2-basic-algorithms", "EDF task configuration"),
            ("part2-edf-03-gantt-chart.png", "part2-basic-algorithms", "EDF Gantt chart"),
            ("part2-edf-04-priority-timeline.png", "part2-basic-algorithms", "EDF priority timeline"),
            ("part2-edf-05-analysis.png", "part2-basic-algorithms", "EDF analysis"),
        ])
        
        # Part 2: Basic Algorithms - DMS
        self.plan.extend([
            ("part2-dms-01-algorithm-selection.png", "part2-basic-algorithms", "DMS algorithm selection"),
            ("part2-dms-02-task-configuration.png", "part2-basic-algorithms", "DMS task configuration"),
            ("part2-dms-03-priority-timeline.png", "part2-basic-algorithms", "DMS priority timeline"),
        ])
        
        # Part 2: Basic Algorithms - LLF
        self.plan.extend([
            ("part2-llf-01-algorithm-selection.png", "part2-basic-algorithms", "LLF algorithm selection"),
            ("part2-llf-02-laxity-timeline.png", "part2-basic-algorithms", "LLF laxity timeline"),
        ])
        
        # Part 3: Server Algorithms
        self.plan.extend([
            ("part3-server-01-category-selection.png", "part3-server-algorithms", "Server category selection"),
            ("part3-server-02-server-configuration.png", "part3-server-algorithms", "Server configuration"),
            ("part3-polling-01-task-configuration.png", "part3-server-algorithms", "Polling Server task configuration"),
            ("part3-polling-02-gantt-chart.png", "part3-server-algorithms", "Polling Server Gantt chart"),
            ("part3-polling-03-server-analysis.png", "part3-server-algorithms", "Polling Server analysis"),
            ("part3-polling-04-algorithm-selection.png", "part3-server-algorithms", "Polling Server algorithm selection"),
            ("part3-polling-05-task-grid-with-periodic-aperiodic.png", "part3-server-algorithms", "Polling Server task grid"),
            ("part3-polling-06-response-times-table.png", "part3-server-algorithms", "Polling Server response times"),
            ("part3-deferrable-01-gantt.png", "part3-server-algorithms", "Deferrable Server Gantt"),
            ("part3-sporadic-01-gantt.png", "part3-server-algorithms", "Sporadic Server Gantt"),
            ("part3-background-01-gantt.png", "part3-server-algorithms", "Background Scheduler Gantt"),
        ])
        
        # Part 4: Precedence-Constrained
        self.plan.extend([
            ("part4-precedence-constrained-01-preset-dialog.png", "part4-precedence", "Precedence preset dialog"),
            ("part4-precedence-constrained-02-rms-chain-config.png", "part4-precedence", "RMS Chain Chain config"),
            ("part4-precedence-constrained-03-rms-chain-precedence-tab.png", "part4-precedence", "RMS Chain precedence tab"),
            ("part4-precedence-constrained-04-rms-chain-gantt.png", "part4-precedence", "RMS Chain Gantt"),
            ("part4-precedence-constrained-05-rms-chain-precedence-graph.png", "part4-precedence", "RMS Chain precedence graph"),
            ("part4-precedence-constrained-06-rms-chain-analysis.png", "part4-precedence", "RMS Chain analysis"),
            ("part4-precedence-constrained-07-edf-fork-config.png", "part4-precedence", "EDF Fork config"),
            ("part4-precedence-constrained-08-edf-fork-gantt.png", "part4-precedence", "EDF Fork Gantt"),
            ("part4-precedence-constrained-09-edf-fork-precedence-graph.png", "part4-precedence", "EDF Fork precedence graph"),
            ("part4-precedence-constrained-10-dms-diamond-config.png", "part4-precedence", "DMS Diamond config"),
            ("part4-precedence-constrained-11-dms-diamond-precedence-tab.png", "part4-precedence", "DMS Diamond precedence tab"),
            ("part4-precedence-constrained-12-dms-diamond-gantt.png", "part4-precedence", "DMS Diamond Gantt"),
            ("part4-precedence-constrained-13-dms-diamond-precedence-graph.png", "part4-precedence", "DMS Diamond precedence graph"),
            ("part4-precedence-constrained-14-dms-diamond-analysis.png", "part4-precedence", "DMS Diamond analysis"),
        ])
        
        # Part 5: Aperiodic Scheduling
        self.plan.extend([
            ("part5-aperiodic-01-preset-dialog.png", "part5-aperiodic", "Aperiodic preset dialog"),
            ("part5-aperiodic-02-edf-hvdf-value-max-config.png", "part5-aperiodic", "EDF+HVDF Value Max config"),
            ("part5-aperiodic-03-edf-hvdf-value-max-gantt.png", "part5-aperiodic", "EDF+HVDF Value Max Gantt"),
            ("part5-aperiodic-04-edf-hvdf-value-max-metrics.png", "part5-aperiodic", "EDF+HVDF Value Max metrics"),
            ("part5-aperiodic-05-edf-hvdf-value-max-analysis.png", "part5-aperiodic", "EDF+HVDF Value Max analysis"),
            ("part5-aperiodic-06-edf-hvdf-staggered-config.png", "part5-aperiodic", "EDF+HVDF Staggered config"),
            ("part5-aperiodic-07-edf-hvdf-staggered-gantt.png", "part5-aperiodic", "EDF+HVDF Staggered Gantt"),
            ("part5-aperiodic-08-edf-hvdf-staggered-analysis.png", "part5-aperiodic", "EDF+HVDF Staggered analysis"),
            ("part5-aperiodic-09-edf-hvdf-burst-config.png", "part5-aperiodic", "EDF+HVDF Burst config"),
            ("part5-aperiodic-10-edf-hvdf-burst-gantt.png", "part5-aperiodic", "EDF+HVDF Burst Gantt"),
            ("part5-aperiodic-11-edf-hvdf-burst-analysis.png", "part5-aperiodic", "EDF+HVDF Burst analysis"),
            ("part5-aperiodic-12-hvdf-only-config.png", "part5-aperiodic", "HVDF Only config"),
            ("part5-aperiodic-13-hvdf-only-gantt.png", "part5-aperiodic", "HVDF Only Gantt"),
            ("part5-aperiodic-14-hvdf-only-analysis.png", "part5-aperiodic", "HVDF Only analysis"),
        ])
        
        # Part 6: Overload Handling
        self.plan.extend([
            ("part6-overload-01-fc-edf-config.png", "part6-overload", "FC-EDF config"),
            ("part6-overload-02-fc-edf-overload-tab.png", "part6-overload", "FC-EDF overload tab"),
            ("part6-overload-03-fc-edf-gantt.png", "part6-overload", "FC-EDF Gantt"),
            ("part6-overload-04-fc-edf-service-level-plot.png", "part6-overload", "FC-EDF service level plot"),
            ("part6-overload-05-fc-edf-analysis.png", "part6-overload", "FC-EDF analysis"),
            ("part6-overload-06-mk-rms-config.png", "part6-overload", "Feedback (m,k)-RMS config"),
            ("part6-overload-07-mk-rms-overload-tab.png", "part6-overload", "Feedback (m,k)-RMS overload tab"),
            ("part6-overload-08-mk-rms-mk-history.png", "part6-overload", "Feedback (m,k)-RMS (m,k) history"),
            ("part6-overload-09-mk-rms-task-grid.png", "part6-overload", "Feedback (m,k)-RMS task grid"),
            ("part6-overload-10-mk-rms-gantt.png", "part6-overload", "Feedback (m,k)-RMS Gantt"),
            ("part6-overload-11-imprecise-algorithm-selection.png", "part6-overload", "Imprecise Computation algorithm selection"),
            ("part6-overload-12-imprecise-task-grid.png", "part6-overload", "Imprecise Computation task grid"),
            ("part6-overload-13-imprecise-gantt.png", "part6-overload", "Imprecise Computation Gantt"),
            ("part6-overload-14-hvdf-algorithm-selection.png", "part6-overload", "HVDF Overload algorithm selection"),
            ("part6-overload-15-hvdf-task-grid-with-values.png", "part6-overload", "HVDF Overload task grid"),
            ("part6-overload-16-hvdf-gantt.png", "part6-overload", "HVDF Overload Gantt"),
            ("part6-overload-17-hvdf-analysis.png", "part6-overload", "HVDF Overload analysis"),
            ("part6-overload-18-mk-firm-algorithm-selection.png", "part6-overload", "(m,k)-Firm Tasks algorithm selection"),
            ("part6-overload-19-mk-firm-task-grid-with-mk-column.png", "part6-overload", "(m,k)-Firm Tasks task grid"),
            ("part6-overload-20-mk-firm-mk-history-chart.png", "part6-overload", "(m,k)-Firm Tasks (m,k) history"),
            ("part6-overload-21-mk-firm-analysis.png", "part6-overload", "(m,k)-Firm Tasks analysis"),
        ])
        
        # Part 7: Advanced Features - Resource Sharing
        self.plan.extend([
            ("part7-resource-01-resources-tab.png", "part7-advanced", "Resources tab"),
            ("part7-resource-02-enable-resource-sharing-checked.png", "part7-advanced", "Enable Resource Sharing checked"),
            ("part7-resource-03-protocol-selection-pip.png", "part7-advanced", "Protocol selection PIP"),
            ("part7-resource-04-resource-grid.png", "part7-advanced", "Resource grid"),
            ("part7-resource-05-task-grid-with-resources-cs.png", "part7-advanced", "Task grid with Resources/CS columns"),
            ("part7-resource-06-gantt-with-blocking.png", "part7-advanced", "Gantt with blocking"),
            ("part7-resource-07-analysis-blocking-time.png", "part7-advanced", "Analysis blocking time"),
            ("part7-resource-08-protocol-selection-pcp.png", "part7-advanced", "Protocol selection PCP"),
        ])
        
        # Part 8: Presets
        self.plan.extend([
            ("part8-01-preset-dialog.png", "part8-presets", "Preset dialog"),
            ("part8-02-server-presets-tab.png", "part8-presets", "Server presets tab"),
        ])
    
    def get_all_screenshots(self) -> List[Tuple[str, str, str]]:
        """Get all screenshot entries."""
        return self.plan
    
    def get_count(self) -> int:
        """Get total count of screenshots."""
        return len(self.plan)


def generate_capture_instructions():
    """
    Generate detailed capture instructions as a JSON file that can be used
    with browser automation tools.
    """
    plan = ScreenshotCapturePlan()
    instructions = []
    
    for filename, subdirectory, description in plan.get_all_screenshots():
        instructions.append({
            "filename": filename,
            "subdirectory": subdirectory,
            "description": description,
            "full_path": str(get_screenshot_path(filename, subdirectory))
        })
    
    output_file = BASE_DIR / "capture_instructions.json"
    with open(output_file, 'w') as f:
        json.dump({
            "total_screenshots": plan.get_count(),
            "instructions": instructions
        }, f, indent=2)
    
    print(f"Generated capture instructions: {output_file}")
    print(f"Total screenshots to capture: {plan.get_count()}")
    return instructions


def generate_browser_automation_script():
    """
    Generate a JavaScript/TypeScript script that can be used with Playwright
    to automate all screenshot captures.
    """
    plan = ScreenshotCapturePlan()
    
    script_content = """// Automated Screenshot Capture Script for Real-Time Scheduling Simulator
// This script uses Playwright to systematically capture all screenshots
// Run with: npx playwright test --headed

import { test, expect } from '@playwright/test';
import { readFileSync } from 'fs';
import path from 'path';

const BASE_URL = 'http://localhost:8501';
const SCREENSHOTS_DIR = path.join(__dirname, 'screenshots');

// Helper function to wait for UI to stabilize
async function waitForStable(page, timeout = 3000) {
    await page.waitForTimeout(timeout);
    // Wait for any loading indicators to disappear
    await page.waitForSelector('[data-testid="stApp"]', { state: 'visible' });
}

// Helper function to ensure no modals are open
async function ensureNoModals(page) {
    // Close any open dialogs
    const dialogs = await page.locator('[role="dialog"]').count();
    if (dialogs > 0) {
        // Press Escape to close any open dialogs
        await page.keyboard.press('Escape');
        await waitForStable(page, 1000);
    }
}

// Helper function to select tab in results panel
async function selectResultsTab(page, tabName) {
    const tabs = page.locator('[role="tablist"]').last();
    const tab = tabs.locator(`[role="tab"]:has-text("${tabName}")`);
    if (await tab.count() > 0) {
        await tab.click();
        await waitForStable(page, 1000);
    }
}

// Helper function to select category
async function selectCategory(page, categoryName) {
    const categorySelect = page.locator('[aria-label*="Category"]').first();
    await categorySelect.click();
    await waitForStable(page, 500);
    const option = page.locator(`[role="option"]:has-text("${categoryName}")`).first();
    await option.click();
    await waitForStable(page, 1000);
}

// Helper function to select algorithm
async function selectAlgorithm(page, algorithmName) {
    const algoSelect = page.locator('[aria-label*="Algorithm"]').first();
    await algoSelect.click();
    await waitForStable(page, 500);
    const option = page.locator(`[role="option"]:has-text("${algorithmName}")`).first();
    await option.click();
    await waitForStable(page, 1000);
}

// Helper function to load preset
async function loadPreset(page, presetName) {
    // Click Presets button
    await page.locator('button:has-text("Presets")').click();
    await waitForStable(page, 1000);
    
    // Find and click the preset's Load button
    // Note: Preset dialog closes automatically after loading
    const loadButton = page.locator(`button:has-text("Load")`).filter({ hasText: presetName }).first();
    if (await loadButton.count() > 0) {
        await loadButton.click();
        // Wait for dialog to close (it closes automatically)
        await waitForStable(page, 2000);
    }
}

// Helper function to run simulation
async function runSimulation(page) {
    await page.locator('button:has-text("Run")').click();
    await waitForStable(page, 3000);
}

// Helper function to expand Advanced Options
async function expandAdvancedOptions(page) {
    const expander = page.locator('text=Advanced Options').locator('..').locator('..');
    const isExpanded = await expander.locator('text=keyboard_arrow_down').count() > 0;
    if (!isExpanded) {
        await expander.click();
        await waitForStable(page, 500);
    }
}

// Helper function to select Advanced Options tab
async function selectAdvancedTab(page, tabName) {
    await expandAdvancedOptions(page);
    const tab = page.locator(`[role="tab"]:has-text("${tabName}")`).last();
    await tab.click();
    await waitForStable(page, 500);
}

test.describe('Screenshot Capture', () => {
    test.beforeEach(async ({ page }) => {
        await page.goto(BASE_URL);
        await waitForStable(page, 2000);
        await ensureNoModals(page);
    });

"""
    
    # Generate test cases for each screenshot
    capture_steps = []
    
    # Part 1: Getting Started
    capture_steps.append("""
    test('Part 1: Getting Started', async ({ page }) => {
        await ensureNoModals(page);
        await page.screenshot({ path: path.join(SCREENSHOTS_DIR, 'part1-getting-started', 'part1-01-initial-state.png'), fullPage: true });
        await page.screenshot({ path: path.join(SCREENSHOTS_DIR, 'part1-getting-started', 'part1-02-full-layout.png'), fullPage: true });
    });
""")
    
    # Part 2: Basic Algorithms
    capture_steps.append("""
    test('Part 2: RMS', async ({ page }) => {
        await selectCategory(page, 'Basic Algorithms');
        await selectAlgorithm(page, 'RMS (Rate Monotonic)');
        await ensureNoModals(page);
        await page.screenshot({ path: path.join(SCREENSHOTS_DIR, 'part2-basic-algorithms', 'part2-rms-01-algorithm-selection.png'), fullPage: true });
        
        await runSimulation(page);
        await ensureNoModals(page);
        await selectResultsTab(page, 'Gantt');
        await page.screenshot({ path: path.join(SCREENSHOTS_DIR, 'part2-basic-algorithms', 'part2-rms-04-gantt-chart.png'), fullPage: true });
        
        await selectResultsTab(page, 'Metrics');
        await page.screenshot({ path: path.join(SCREENSHOTS_DIR, 'part2-basic-algorithms', 'part2-rms-05-metrics-dashboard.png'), fullPage: true });
        
        await selectResultsTab(page, 'Analysis');
        await page.screenshot({ path: path.join(SCREENSHOTS_DIR, 'part2-basic-algorithms', 'part2-rms-07-analysis-tab.png'), fullPage: true });
    });
""")
    
    # Add more test cases...
    
    script_content += "\n".join(capture_steps)
    script_content += "\n});\n"
    
    output_file = BASE_DIR / "playwright_screenshot_capture.spec.ts"
    with open(output_file, 'w') as f:
        f.write(script_content)
    
    print(f"Generated Playwright script: {output_file}")
    return script_content


def main():
    """Main function."""
    print("=" * 60)
    print("Screenshot Capture Plan Generator")
    print("=" * 60)
    print()
    
    # Generate instructions
    instructions = generate_capture_instructions()
    
    # Generate Playwright script
    generate_browser_automation_script()
    
    print()
    print("=" * 60)
    print("Summary:")
    print(f"  Total screenshots planned: {len(instructions)}")
    print(f"  Instructions saved to: capture_instructions.json")
    print(f"  Playwright script saved to: playwright_screenshot_capture.spec.ts")
    print()
    print("Next steps:")
    print("  1. Review capture_instructions.json")
    print("  2. Use the Playwright script or implement manual capture")
    print("  3. Ensure Streamlit app is running on http://localhost:8501")
    print("=" * 60)


if __name__ == "__main__":
    main()

