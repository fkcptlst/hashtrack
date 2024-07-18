import hashlib
import json
import os
import time
from pathlib import Path
from typing import Tuple

import yaml
from addict import Dict

from hashtrack.utils.constants import TRACK_DIR, FileStatus


def get_file_status(cache, f) -> Tuple[FileStatus, str]:
    if isinstance(f, str):
        f = Path(f)

    if not f.exists():
        return FileStatus.REMOVED, "-" * 32

    md5 = hashlib.md5(f.read_bytes()).hexdigest()

    if not str(f) in cache:  # new file
        return FileStatus.NEW, md5
    else:  # existing file
        if cache[str(f)]["md5"] != md5:
            if cache[str(f)]["modified"] < f.stat().st_mtime:
                return FileStatus.MODIFIED, md5
            return FileStatus.CORRUPTED, md5

        return FileStatus.UNCHANGED, md5


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
    config = Dict(config)

    if "." in config.search_dirs:
        print("------------------ WARNING ------------------\n"
              "Detected '.' in search_dirs.\n"
              "This is the default behavior. However, it is recommended to specify the search directories (checkpoint directories) explicitly to increase efficiency.\n"
              "Example:\n"
              "\t`hashtrack config add --search_dirs=your_checkpoint_dir`\n"
              "\t`hashtrack config remove '.'`\n"
              "---------------------------------------------\n")

    return config


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
