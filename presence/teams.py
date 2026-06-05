import re
from pathlib import Path

from .base import PresenceProvider, PresenceStatus

_LOG_DIR = Path.home() / "Library/Group Containers/UBF8T346G9.com.microsoft.teams/Library/Application Support/Logs"
_AVAILABILITY_RE = re.compile(r"BroadcastGlobalState.*?availability:\s*(\w+)")


def _latest_log() -> Path:
    logs = sorted(_LOG_DIR.glob("MSTeams_*.log"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not logs:
        raise FileNotFoundError(f"No MSTeams log files found in {_LOG_DIR}")
    return logs[0]


def _read_availability() -> str:
    log = _latest_log()
    last_match = None
    with log.open(errors="replace") as f:
        for line in f:
            m = _AVAILABILITY_RE.search(line)
            if m:
                last_match = m.group(1)
    if last_match is None:
        raise ValueError(f"No availability found in {log.name}")
    return last_match


class TeamsPresence(PresenceProvider):
    def get_status(self) -> PresenceStatus:
        availability = _read_availability()
        return PresenceStatus(
            platform="Teams",
            availability=availability,
            activity="Unknown",  # log doesn't include activity detail
        )
