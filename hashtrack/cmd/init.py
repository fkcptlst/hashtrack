import json
import shutil
from pathlib import Path

from hashtrack import cli
from hashtrack.utils.constants import TRACK_DIR, CACHE_PATH, CONFIG_DEFAULT_PATH, CONFIG_PATH


@cli.command()
def init():
    """Initialize hashtrack cache"""
    if Path(TRACK_DIR).exists():
        print("hashtrack cache already exists.")
        return

    # Initialize TRACK_DIR
    Path(TRACK_DIR).mkdir(parents=True)

    # Copy default config.yml
    shutil.copy(CONFIG_DEFAULT_PATH, CONFIG_PATH)

    # Initialize empty cache
    with open(CACHE_PATH, "w") as f:
        json.dump({}, f)

    # if .gitignore exists, append TRACK_DIR
    gitignore_path = Path(".gitignore")
    if gitignore_path.exists():
        with open(gitignore_path, "a") as f:
            f.write(f"\n{TRACK_DIR}\n")

    print("hashtrack cache initialized.")
