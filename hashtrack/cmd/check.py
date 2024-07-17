from pathlib import Path

import click

from hashtrack import cli
from hashtrack.utils.constants import CACHE_PATH
from hashtrack.utils.log import log_modified, log_removed, log_unchanged
from hashtrack.utils.misc import abort_if_cache_not_initialized, load_cache, get_info


@cli.command()
@click.option("-f", "--file", type=str, default="", help="File to check.")
@click.option("-v", "--verbose", is_flag=True, default=False, help="Print verbose output.")
def check(file, verbose):
    """Check if entries in cache is modified (or corrupted)"""
    abort_if_cache_not_initialized()

    cache = load_cache(CACHE_PATH)

    if file:
        if Path(file).is_file():
            if Path(file).is_absolute():  # if is_absolute, convert to relative path
                file = Path(file).relative_to(Path.cwd())
            if str(file) in cache:
                if cache[str(file)]["md5"] == get_info(file)["md5"]:
                    log_unchanged(f"{file}")
                else:
                    log_modified(f"{file}")
            else:
                log_removed(f"{file}")
        else:
            print("You must provide a valid file path (not a directory).")

        return

    modified, removed, unchanged = 0, 0, 0

    for k, v in cache.items():
        if not Path(k).is_file():
            log_removed(f"{k}")
            removed += 1
        else:
            if v["md5"] != get_info(k)["md5"]:
                log_modified(f"{k}")
                modified += 1
                continue

            unchanged += 1
            if verbose:
                log_unchanged(f"{k}")

    print(f"Modified: {modified}, Removed: {removed}, Unchanged: {unchanged}")