# meeting_presence

Reads the current user's presence/status from communication platforms and drives output devices (USB status light, etc.).

## Purpose

Check whether the user is currently in a meeting or otherwise busy. Intended for personal automation (e.g. drive an Embrava Blynclight, suppress notifications, block distractions when in a meeting).

## Platforms

- **Microsoft Teams** — reads presence from local Teams log files (no auth required)
- **Slack** — not yet implemented; may be added later

## How Teams presence works

Teams writes availability changes to a local log file in real time, and also emits a heartbeat every ~5 minutes. We parse the latest `MSTeams_*.log` file for `BroadcastGlobalState` lines containing `availability: <value>`.

Log location:
```
~/Library/Group Containers/UBF8T346G9.com.microsoft.teams/Library/Application Support/Logs/MSTeams_*.log
```

No auth, no network calls, no app registration needed.

## Structure

```
meeting_presence/
├── CLAUDE.md
├── README.md
├── requirements.txt
├── presence/
│   ├── __init__.py
│   ├── teams.py       # reads Teams local log
│   └── base.py        # PresenceProvider ABC + PresenceStatus dataclass
├── effects/
│   ├── __init__.py
│   ├── base.py        # StatusEffect ABC
│   └── blynclight.py  # Embrava Blynclight USB light
└── main.py            # polling loop, wires providers + effects
```

## Presence values

Teams `availability` field: `Available`, `Busy`, `DoNotDisturb`, `BeRightBack`, `Away`, `Offline`, `PresenceUnknown`

Note: the local log does not include the `activity` field (InAMeeting, InACall, etc.) — only availability.

## macOS permissions

Terminal/Python needs access to the Teams Group Container. Grant **Full Disk Access** to the Python binary in System Settings → Privacy & Security if running from cron or a background process.

## Running

```bash
.venv/bin/python main.py
```
