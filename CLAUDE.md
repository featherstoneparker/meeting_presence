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
├── run.sh                 # shell wrapper (used during debugging, not primary entry point)
├── presence/
│   ├── __init__.py
│   ├── teams.py           # reads Teams local log
│   └── base.py            # PresenceProvider ABC + PresenceStatus dataclass
├── effects/
│   ├── __init__.py
│   ├── base.py            # StatusEffect ABC
│   └── blynclight.py      # Embrava Blynclight USB light
├── logs/
│   ├── output.log         # LaunchAgent stdout
│   └── error.log          # LaunchAgent stderr
└── main.py                # polling loop, wires providers + effects
```

## Python version

Must use **Homebrew Python 3.9** (`/opt/homebrew/opt/python@3.9/bin/python3.9`):
- `blynclight` library uses `collections.Sequence` which was removed in Python 3.10
- System Python (`com.apple.python3`) cannot receive the required macOS TCC permission when running as a background LaunchAgent — macOS silently ignores TCC grants for Apple-signed binaries in that context. Homebrew Python (unsigned) triggers a proper user-facing prompt that sticks.

## macOS TCC permissions

The Teams log directory is protected by macOS's "Other Apps' Data" TCC permission (`kTCCServiceSystemPolicyAppData`). Key findings:

- When running interactively from iTerm2, the permission passes through from iTerm2 (the responsible process) — no separate Python permission is created
- LaunchAgents run outside the GUI responsible-process chain, so they need their OWN TCC entry
- System Python (`com.apple.python3`) TCC entries are ignored by `tccd` even when manually inserted — Apple-signed binaries are handled differently
- Homebrew Python (unsigned, `TeamIdentifier=not set`) can receive and hold the permission normally
- To force the TCC prompt for the LaunchAgent context: `tccutil reset SystemPolicyAppData`, then restart the LaunchAgent — the prompt appears on screen and clicking Allow creates a persistent entry for the Homebrew Python binary

## LaunchAgent

Installed at `~/Library/LaunchAgents/com.yourname.meeting-presence.plist`. Loaded with:
```bash
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.yourname.meeting-presence.plist
```

Managed with:
```bash
launchctl kickstart -k gui/$(id -u)/com.yourname.meeting-presence  # restart
launchctl print gui/$(id -u)/com.yourname.meeting-presence          # status
```

Code changes are not picked up automatically — restart the service after any edits.

## Presence values

Teams `availability` field: `Available`, `Busy`, `DoNotDisturb`, `BeRightBack`, `Away`, `Offline`, `PresenceUnknown`

Note: the local log does not include the `activity` field (InAMeeting, InACall, etc.) — only availability.

## Testing colors

`test_color.py` sets the Blynclight to any hex color directly, useful for dialing in color values without touching the service. Stop the service first (it holds exclusive USB access), test colors, then restart.

Will be extended to support Govee LAN once the bulb is available.

## Running manually

```bash
.venv/bin/python main.py
```
