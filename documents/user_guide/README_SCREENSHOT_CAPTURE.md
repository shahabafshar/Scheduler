# Screenshot Capture Automation

Scripts for capturing screenshots are located in the `tools/` folder at the project root.

## Scripts

### 1. `tools/capture_all_screenshots.py`
**Main automation script using Playwright**

This script systematically captures all screenshots, ensuring:
- No modals/dialogs are open when capturing
- Correct tabs are selected before capturing
- UI is stable before each screenshot
- Previous screenshots are overwritten
- Statistics are reported (new files, replacements, errors)

**Requirements:**
```bash
pip install playwright
playwright install chromium
```

**Usage:**
```bash
# Make sure Streamlit app is running on http://localhost:8501
cd tools
python capture_all_screenshots.py

# Resume from a specific part
python capture_all_screenshots.py --start-from 3

# Run only a specific part
python capture_all_screenshots.py --part 2
```

**Features:**
- Automatically waits for UI to stabilize
- Closes any open modals before capturing
- Selects correct tabs (Gantt, Metrics, Analysis, etc.)
- Handles preset loading (dialog closes automatically)
- Reports statistics on completion
- Resume functionality (--start-from, --part flags)

### 2. `tools/automated_screenshot_capture.py`
**Plan generator and instruction creator**

Generates:
- `capture_instructions.json`: Complete list of all screenshots to capture
- `playwright_screenshot_capture.spec.ts`: TypeScript/Playwright test file template

**Usage:**
```bash
cd tools
python automated_screenshot_capture.py
```

## Screenshot Organization

Screenshots are organized by part:

- `part1-getting-started/` - Initial UI and layout
- `part2-basic-algorithms/` - RMS, EDF, DMS, LLF
- `part3-server-algorithms/` - Polling, Deferrable, Sporadic, Background
- `part4-precedence/` - Precedence-constrained algorithms
- `part5-aperiodic/` - Aperiodic scheduling algorithms
- `part6-overload/` - Overload handling algorithms
- `part7-advanced/` - Resource sharing, advanced features
- `part8-presets/` - Preset system documentation

## Important Notes

### Modal Handling
- **Preset Dialog**: Closes automatically after clicking "Load" - no need to click "Close"
- **Always check for modals**: Script ensures no dialogs are open before capturing

### Tab Selection
- **Results Panel Tabs**: Gantt, Metrics, Timeline, Analysis, Export
- **Advanced Options Tabs**: Resources, Precedence, Overload
- Script automatically selects the correct tab before capturing

### State Management
- Script waits for UI to stabilize (2-3 seconds)
- Ensures simulation has completed before capturing results
- Verifies no loading indicators are present

## Troubleshooting

### Common Issues

1. **Modal blocking view**
   - Script automatically closes modals with Escape key
   - If issue persists, check for custom dialogs

2. **Wrong tab selected**
   - Script explicitly selects tabs before capturing
   - Verify tab names match exactly

3. **UI not loaded**
   - Increase wait times in `wait_for_stable()` function
   - Check Streamlit app is fully loaded

4. **Preset not found**
   - Verify preset name matches exactly (case-sensitive)
   - Check preset exists in `PRESET_CATALOG`

## Statistics

After running `capture_all_screenshots.py`, you'll see:
- **Total screenshots**: Total number captured
- **New files**: Files that didn't exist before
- **Replaced files**: Files that were overwritten
- **Errors**: Number of failed captures

## Next Steps

1. Run `capture_all_screenshots.py` to capture all screenshots
2. Review statistics to identify any issues
3. Re-run specific parts if needed
4. Use `organize_screenshots.py` if capturing manually via browser extension

