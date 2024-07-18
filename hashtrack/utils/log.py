import sys

from loguru import logger

from hashtrack.utils.constants import FileStatus

level_unchanged = logger.level("UNCHANGED", no=20, color="<green>")
level_new = logger.level("NEW", no=20, color="<blue>")
level_modified = logger.level("MODIFIED", no=20, color="<cyan>")
level_removed = logger.level("REMOVED", no=20, color="<yellow>")
level_corrupted = logger.level("CORRUPTED", no=20, color="<red>")

logger.remove()

logger.add(sys.stdout, colorize=True, format="[<level>{level:^11}</level>] {message}")
logger = logger.opt(ansi=True)

_map = {
    FileStatus.UNCHANGED: "UNCHANGED",
    FileStatus.NEW: "NEW",
    FileStatus.MODIFIED: "MODIFIED",
    FileStatus.REMOVED: "REMOVED",
    FileStatus.CORRUPTED: "CORRUPTED",
}


def log_file_status(file_status, message):
    logger.log(_map[file_status], message)


def make_fmt_log():
    """
    Make a closure for logging file status.
    """
    first_call = True

    def inner(file_status: FileStatus, md5: str, file_path: str, skipped_update=False):
        nonlocal first_call
        # [status] [md5:keep 5 chars] [file_path]
        if first_call:
            first_call = False
            print(f"{'Status':<13} {'MD5':<5} {'File Path':<50}")

        log_file_status(file_status,
                        f"{md5[:5]} {file_path: <50}{'<yellow>(skipped)</yellow>' if skipped_update else ''}")

    return inner


fmt_log = make_fmt_log()
