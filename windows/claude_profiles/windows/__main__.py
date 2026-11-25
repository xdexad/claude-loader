"""`python -m claude_profiles.windows` = the claude-profiles command on Windows."""

import sys


def _attach_log() -> None:
    """pythonw.exe started from a shortcut (Start menu, Desktop, Startup folder) has
    no stdout/stderr at all: they are None, so any write would crash it silently.
    Send them to a log instead, so an error leaves a traceback behind."""
    if sys.stdout is not None and sys.stderr is not None:
        return
    import time
    from ..core import paths
    log = None
    try:
        paths.LOG_DIR.mkdir(parents=True, exist_ok=True)
        path = paths.LOG_DIR / "claude-profiles.log"
        if path.exists() and path.stat().st_size > 512 * 1024:
            path.replace(path.with_suffix(".log.old"))
        log = open(path, "a", encoding="utf-8", errors="replace", buffering=1)
    except OSError:
        pass
    if log is None:
        import os
        log = open(os.devnull, "w")
    if sys.stdout is None:
        sys.stdout = log
    if sys.stderr is None:
        sys.stderr = log

    def excepthook(kind, value, tb):
        import traceback
        log.write(f"\n{time.strftime('%Y-%m-%d %H:%M:%S')} claude-profiles "
                  f"{' '.join(sys.argv[1:])}\n")
        traceback.print_exception(kind, value, tb, file=log)
        log.flush()

    sys.excepthook = excepthook


if __name__ == "__main__":
    _attach_log()
    from ..core.cli import main
    from .platform import WindowsPlatform
    sys.exit(main(WindowsPlatform()))
