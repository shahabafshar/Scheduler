"""
Script to organize screenshots from temp directory to proper structure.
Tracks replacements and reports statistics.
"""
import shutil
from pathlib import Path
import glob

TEMP_DIR = Path(r"C:\Users\shahab\AppData\Local\Temp\cursor-browser-extension")
TARGET_DIR = Path(__file__).parent / "screenshots"

STATS = {
    "total": 0,
    "replaced": 0,
    "new": 0,
    "errors": 0
}

def organize_screenshots():
    """Move screenshots from temp to organized structure."""
    # Find all PNG files in temp directory
    png_files = list(TEMP_DIR.glob("**/*.png"))
    
    if not png_files:
        print("No PNG files found in temp directory.")
        return
    
    print(f"Found {len(png_files)} PNG file(s) to organize...\n")
    
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
        
        # Check if file already exists
        existed = target.exists()
        
        try:
            shutil.copy2(png_file, target)
            STATS["total"] += 1
            if existed:
                STATS["replaced"] += 1
                print(f"  [REPLACED] {filename} -> {target.relative_to(TARGET_DIR.parent)}")
            else:
                STATS["new"] += 1
                print(f"  [NEW] {filename} -> {target.relative_to(TARGET_DIR.parent)}")
        except Exception as e:
            STATS["errors"] += 1
            print(f"  [ERROR] {filename} - {e}")
    
    # Print statistics
    print("\n" + "=" * 60)
    print("Organization Statistics:")
    print(f"  Total files processed: {STATS['total']}")
    print(f"  New files: {STATS['new']}")
    print(f"  Replaced files: {STATS['replaced']}")
    print(f"  Errors: {STATS['errors']}")
    print("=" * 60)

if __name__ == "__main__":
    organize_screenshots()

