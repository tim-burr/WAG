# Imports
# Standard
import sys
from pathlib import Path
# Local
import utils.drive_tools as drive
import utils.config_loader as cfg
import utils.generator as gen

# Directories
CONF_DIR = Path(__file__).parents[1].resolve()

# Files
DEF_CONFIG = CONF_DIR / "config.yml"  # Default build config

########################
# Main
########################
if __name__=="__main__":
    # Handle program inputs
    try:
        file = sys.argv[1]
    except IndexError:
        print("Empty or invalid configuration input... Trying default")
        file = DEF_CONFIG
        
    # Load build config data
    config = cfg.Configuration(file)
    
    # Buffer directory paths from config data
    page_dir = config.paths.get("pages")
    build_dir = config.paths.get("build")

    # Remove old build directory, if exists
    drive.delete_directory(build_dir)
    # Create new, empty build directory
    drive.create_directory(build_dir)

    # Directly copy Includes into build directory
    for i, path in enumerate(config.includes):
        drive.copy_recursive(path, build_dir)

    # Generate one HTML file per found source file
    run = gen.Generator(config)
    website = page_dir.rglob("*.md")
    
    for page in website:
        run.generate(page)

    print("\nWebsite generated!\n")
