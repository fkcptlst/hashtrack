import json

from hashtrack import cli
from hashtrack.utils.constants import CACHE_PATH
from hashtrack.utils.misc import abort_if_cache_not_initialized, load_cache


@cli.group()
def cache():
    """Operations on the cache."""
    ...


@cache.command()
def clear():
    """Clear all entries in the cache."""
    abort_if_cache_not_initialized()

    cache = load_cache(CACHE_PATH)

    key = input(f"Are you sure you want to clear {len(cache)} entries in the cache? [y/n]: ")
    if key.lower() != "y":
        print("Aborted.")
        return

    with open(CACHE_PATH, "w") as f:
        json.dump({}, f)

    print("Cache cleared.")


@cache.command()
def ls():
    """List all entries in the cache."""
    abort_if_cache_not_initialized()

    cache = load_cache(CACHE_PATH)

    for k, v in cache.items():
        print(f"{k} -> {v}")
