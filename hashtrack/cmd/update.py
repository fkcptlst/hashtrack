import hashlib
import json
from pathlib import Path

import click

from hashtrack import cli
from hashtrack.utils.constants import CACHE_PATH, CONFIG_PATH
from hashtrack.utils.log import log_new, log_modified, log_removed
from hashtrack.utils.misc import abort_if_cache_not_initialized, load_config, load_cache, rglob, write_cache_


@cli.command()
@click.option("--strict", is_flag=True, default=False,
              help="Only allows adding new entries, not modifying existing ones.")
def update(strict):
    """Scan for new/modified/removed files and update the cache."""
    print(f"Updating cache{' (strict)' if strict else ''}...")

    abort_if_cache_not_initialized()
    cfg = load_config(CONFIG_PATH)

    search_dirs = set([Path(d) for d in cfg.search_dirs])

    matched_files = []
    for d in search_dirs:
        for f in rglob(str(d), cfg.extensions):
            if f.is_file():
                matched_files.append(f)

    cache = load_cache(CACHE_PATH)

    cache_modified = False

    for f in matched_files:
        md5 = hashlib.md5(f.read_bytes()).hexdigest()
        if not str(f) in cache:  # new file
            log_new(f"{f}")
            write_cache_(cache, rel_path=f, md5=md5)
            cache_modified = True
        else:  # existing file
            if cache[str(f)]["md5"] != md5:
                if strict:
                    log_modified(f"{f} (skipped)")
                else:
                    log_modified(f"{f}")
                    write_cache_(cache, rel_path=f, md5=md5)
                    cache_modified = True

    # check for removed files
    removed_files = set(cache.keys()) - set([str(f) for f in matched_files])
    for f in removed_files:
        if strict:
            log_removed(f"{f} (skipped)")
        else:
            log_removed(f"{f}")
            del cache[f]
            cache_modified = True

    if not cache_modified:
        print("Cache not updated.")
        return

    key = input("Update cache? [y/n]: ")
    if key.lower() == "y":
        with open(CACHE_PATH, "w") as f:
            json.dump(cache, f, indent=4)
        print("Cache updated.")
    else:
        print("Cache not updated.")
