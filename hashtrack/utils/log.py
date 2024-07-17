import sys

from loguru import logger

level_unchanged = logger.level("UNCHANGED", no=20, color="<green>")
level_new = logger.level("NEW", no=20, color="<blue>")
level_modified = logger.level("MODIFIED", no=20, color="<red>")
level_removed = logger.level("REMOVED", no=20, color="<yellow>")

logger.remove()

logger.add(sys.stdout, colorize=True, format="[<level>{level}</level>] {message}")


def log_unchanged(message):
    logger.log("UNCHANGED", message)


def log_new(message):
    logger.log("NEW", message)


def log_modified(message):
    logger.log("MODIFIED", message)


def log_removed(message):
    logger.log("REMOVED", message)
