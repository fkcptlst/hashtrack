import shutil
from pathlib import Path

import click
import yaml

from hashtrack import cli
from hashtrack.utils.constants import TRACK_DIR, CONFIG_PATH
from hashtrack.utils.misc import abort_if_cache_not_initialized, load_config


@cli.group()
def config():
    """Configuration commands"""
    ...


@config.command()
def reset():
    """Reset the configuration"""
    abort_if_cache_not_initialized()
    shutil.copy(Path(__file__).parent.parent / "config.yml", TRACK_DIR / "config.yml")
    print("Configuration reset to default.")


@config.command()
@click.option("--extensions", type=str, default="", help="Comma-separated list of file extensions to track.")
@click.option("--search_dirs", type=str, default="", help="Comma-separated list of directories to search for files.")
def add(extensions, search_dirs):
    """Add a new configuration entry"""
    abort_if_cache_not_initialized()
    cfg = load_config(CONFIG_PATH)

    if extensions:
        for ext in extensions.split(","):
            if ext.strip() not in cfg.extensions:
                cfg.extensions.append(ext.strip())

    if search_dirs:
        for d in search_dirs.split(","):
            if d.strip() not in cfg.search_dirs:
                cfg.search_dirs.append(d.strip())

    with open(CONFIG_PATH, "w") as f:
        yaml.dump(dict(cfg), f, default_flow_style=False)

    print("Configuration updated.")


@config.command()
@click.option("--extensions", type=str, default="", help="Comma-separated list of file extensions to track.")
@click.option("--search_dirs", type=str, default="", help="Comma-separated list of directories to search for files.")
def remove(extensions, search_dirs):
    """Remove a configuration entry"""
    abort_if_cache_not_initialized()
    cfg = load_config(CONFIG_PATH)

    if extensions:
        for ext in extensions.split(","):
            if ext.strip() in cfg.extensions:
                cfg.extensions.remove(ext.strip())

    if search_dirs:
        for d in search_dirs.split(","):
            if d.strip() in cfg.search_dirs:
                cfg.search_dirs.remove(d.strip())

    with open(CONFIG_PATH, "w") as f:
        yaml.dump(dict(cfg), f, default_flow_style=False)

    print("Configuration updated.")


@config.command()
def show():
    """Show the current configuration"""
    abort_if_cache_not_initialized()
    cfg = load_config(CONFIG_PATH)
    print(yaml.dump(dict(cfg), default_flow_style=False))
