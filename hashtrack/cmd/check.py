import hashlib
from collections import defaultdict
from pathlib import Path

import click

from hashtrack import cli
from hashtrack.utils.constants import CACHE_PATH, FileStatus
from hashtrack.utils.log import fmt_log
from hashtrack.utils.misc import abort_if_cache_not_initialized, load_cache, get_file_status


@cli.command()
@click.option("-f", "--file", type=str, default="", help="File to check.")
@click.option("-v", "--verbose", is_flag=True, default=False, help="Print verbose output.")
def check(file, verbose):
    """Check if entries in cache is modified (or corrupted)"""
    abort_if_cache_not_initialized()

    cache = load_cache(CACHE_PATH)

    if file:
        file = Path(file)
        if file.is_file():
            if file.is_absolute():  # if is_absolute, convert to relative path
                file = file.relative_to(Path.cwd())

            file_status, md5 = get_file_status(cache, file)
            fmt_log(file_status, md5, str(file))
        else:
            print("You must provide a valid file path (not a directory).")

        return

    counter = defaultdict(int)

    for k, v in cache.items():
        file_status, md5 = get_file_status(cache, Path(k))
        counter[file_status] += 1

        if not verbose and file_status == FileStatus.UNCHANGED:
            continue
        fmt_log(file_status, md5, k)

    print(f"\nSummary:\n"
          f"Unchanged: {counter[FileStatus.UNCHANGED]}\n"
          f"New: {counter[FileStatus.NEW]}\n"
          f"Modified: {counter[FileStatus.MODIFIED]}\n"
          f"Removed: {counter[FileStatus.REMOVED]}\n"
          f"Corrupted: {counter[FileStatus.CORRUPTED]}")
