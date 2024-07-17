from pathlib import Path

TRACK_DIR = Path(".hashtrack")
CACHE_PATH = TRACK_DIR / "cache.json"
CONFIG_DEFAULT_PATH = Path(__file__).parent.parent / "config.yml"
CONFIG_PATH = TRACK_DIR / "config.yml"