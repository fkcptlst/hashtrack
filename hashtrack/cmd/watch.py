import json
import time
from pathlib import Path

import click

from hashtrack import cli
from hashtrack.utils.constants import CACHE_PATH, CONFIG_PATH, FileStatus
from hashtrack.utils.log import fmt_log
from hashtrack.utils.misc import (
    abort_if_cache_not_initialized,
    load_config,
    load_cache,
    rglob,
    write_cache_,
    get_file_status
)


@cli.command()
@click.option("--strict", is_flag=True, default=False,
              help="Only allows adding new entries, not modifying existing ones.")
def watch(strict):
    """Scan for new/modified/removed files and update the cache continuously."""
    print(f"Watching for changes{' (strict)' if strict else ''}...")
    abort_if_cache_not_initialized()
    cfg = load_config(CONFIG_PATH)

    cache = load_cache(CACHE_PATH)

    search_dirs = set([Path(d) for d in cfg.search_dirs])

    cache_modified = False

    while True:
        file_paths = []
        for d in search_dirs:
            for f in rglob(str(d), cfg.extensions):
                file_paths.append(f)

                file_status, md5 = get_file_status(cache, f)
                if file_status == FileStatus.UNCHANGED:
                    continue
                if strict and file_status != FileStatus.NEW:  # only allow adding new entries
                    fmt_log(file_status, md5, str(f), skipped_update=True)
                    continue

                if file_status == FileStatus.CORRUPTED:
                    fmt_log(file_status, md5, str(f), skipped_update=True)
                    continue
                elif (
                        file_status == FileStatus.MODIFIED
                        and time.time() - f.stat().st_mtime > cfg.watch.min_update_interval
                ):
                    # Update cache
                    write_cache_(cache, rel_path=f, md5=md5)
                    cache_modified = True
                    fmt_log(file_status, md5, str(f))

        remaining_files = set(cache.keys()) - set([str(f) for f in file_paths])
        for f in remaining_files:
            file_status, md5 = FileStatus.REMOVED, "-" * 32
            if strict:
                fmt_log(file_status, md5, f, skipped_update=True)
                continue

            fmt_log(file_status, md5, f)
            del cache[str(f)]
            cache_modified = True

        if cache_modified:
            with open(CACHE_PATH, "w") as f:
                json.dump(cache, f, indent=4)
            cache_modified = False
            print("Cache updated.")

        time.sleep(cfg.watch.sleep_interval)
