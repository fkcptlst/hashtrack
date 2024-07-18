import json
import os
import time
from pathlib import Path

import yaml
from addict import Dict

from hashtrack.utils.constants import TRACK_DIR


def abort_if_cache_not_initialized():
    """Check if the cache is initialized"""
    if not Path(TRACK_DIR).exists():
        print("hashtrack cache not initialized. Run `hashtrack init`.")
        exit(1)


def rglob(directory, extensions):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if f".{file.split('.')[-1]}" in extensions:
                yield Path(root) / file


def load_config(config_path: Path) -> Dict:
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    return Dict(config)


def load_cache(cache_path: Path) -> Dict:
    with open(cache_path, "r") as f:
        cache = json.load(f)
    return cache


def write_cache_(cache, *, rel_path, md5):
    if isinstance(rel_path, str):
        rel_path = Path(rel_path)

    cache[str(rel_path)] = {
        "name": rel_path.name,
        "modified": rel_path.stat().st_mtime,
        "md5": md5,
        "cache_updated_at": time.time()
    }

    return cache
