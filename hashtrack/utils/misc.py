import hashlib
import json
import os
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


def get_info(file_path):
    """Get the information of a file."""
    if isinstance(file_path, str):
        file_path = Path(file_path)

    return {
        "name": file_path.name,
        "modified": file_path.stat().st_mtime,
        "md5": hashlib.md5(file_path.read_bytes()).hexdigest(),
    }
