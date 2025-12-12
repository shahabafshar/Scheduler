"""
Script to organize screenshots from temp directory to proper structure.
"""
import shutil
from pathlib import Path
import glob

TEMP_DIR = Path(r"C:\Users\shahab\AppData\Local\Temp\cursor-browser-extension")
TARGET_DIR = Path(__file__).parent / "screenshots"

def organize_screenshots():
    """Move screenshots from temp to organized structure."""
    # Find all PNG files in temp directory
    png_files = list(TEMP_DIR.glob("**/*.png"))
    
    for png_file in png_files:
        filename = png_file.name
        # Determine target directory based on filename
        if filename.startswith("part1-"):
            target = TARGET_DIR / "part1-getting-started" / filename
        elif filename.startswith("part2-"):
            target = TARGET_DIR / "part2-basic-algorithms" / filename
        elif filename.startswith("part3-"):
            target = TARGET_DIR / "part3-server-algorithms" / filename
        elif filename.startswith("part4-"):
            target = TARGET_DIR / "part4-precedence" / filename
        elif filename.startswith("part5-"):
            target = TARGET_DIR / "part5-aperiodic" / filename
        elif filename.startswith("part6-"):
            target = TARGET_DIR / "part6-overload" / filename
        elif filename.startswith("part7-"):
            target = TARGET_DIR / "part7-advanced" / filename
        elif filename.startswith("part8-"):
            target = TARGET_DIR / "part8-presets" / filename
        elif filename.startswith("part9-"):
            target = TARGET_DIR / "part9-visualizations" / filename
        elif filename.startswith("part10-"):
            target = TARGET_DIR / "part10-analysis" / filename
        elif filename.startswith("part11-"):
            target = TARGET_DIR / "part11-export" / filename
        elif filename.startswith("part12-"):
            target = TARGET_DIR / "part12-config" / filename
        elif filename.startswith("part13-"):
            target = TARGET_DIR / "part13-errors" / filename
        elif filename.startswith("part14-"):
            target = TARGET_DIR / "part14-workflows" / filename
        elif filename.startswith("part15-"):
            target = TARGET_DIR / "part15-comparisons" / filename
        else:
            target = TARGET_DIR / filename
        
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(png_file, target)
        print(f"Moved: {filename} -> {target}")

if __name__ == "__main__":
    organize_screenshots()
