# meeting_presence

Reads your Microsoft Teams presence status from local log files and drives an Embrava Blynclight USB status light. No cloud auth required — works entirely offline by parsing Teams' local logs.

## How it works

Teams writes presence changes (Available, Busy, DoNotDisturb, etc.) to a local log file in real time. This script tails that log every 5 seconds and updates the light color accordingly.

## Requirements

- macOS
- Microsoft Teams (new Teams 2.0)
- Embrava Blynclight connected via USB
- Homebrew Python 3.9 exactly (see below — version matters)

## Setup

### 1. Install Homebrew Python 3.9

You must use **Homebrew Python 3.9** specifically:
- The `blynclight` library is incompatible with Python 3.10+ (uses removed `collections.Sequence`)
- System Python (`com.apple.python3`) cannot be granted the required macOS privacy permission when running as a background process — Homebrew Python can

```bash
brew install python@3.9
```

### 2. Create the venv and install dependencies

```bash
/opt/homebrew/opt/python@3.9/bin/python3.9 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

### 3. Run manually first

```bash
.venv/bin/python main.py
```

macOS will prompt: **"python3.9 would like to access data from other apps"** — click **Allow**. This grants access to the Teams log directory.

## Running as a LaunchAgent (start at login)

The LaunchAgent plist is at `~/Library/LaunchAgents/com.yourname.meeting-presence.plist`. Create it with:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.yourname.meeting-presence</string>
    <key>ProgramArguments</key>
    <array>
        <string>/path/to/meeting_presence/.venv/bin/python</string>
        <string>-u</string>
        <string>/path/to/meeting_presence/main.py</string>
    </array>
    <key>WorkingDirectory</key>
    <string>/path/to/meeting_presence</string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/path/to/meeting_presence/logs/output.log</string>
    <key>StandardErrorPath</key>
    <string>/path/to/meeting_presence/logs/error.log</string>
</dict>
</plist>
```

### Granting the LaunchAgent TCC permission

The LaunchAgent runs outside the GUI session, so macOS won't automatically reuse the permission you granted interactively. To force the prompt to appear for the background process:

1. Reset all "Other Apps Data" permissions:
   ```bash
   tccutil reset SystemPolicyAppData
   ```
2. Load and start the LaunchAgent:
   ```bash
   launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.yourname.meeting-presence.plist
   launchctl kickstart -k gui/$(id -u)/com.yourname.meeting-presence
   ```
3. A prompt will appear on screen — click **Allow**

The permission is now permanently granted to the Homebrew Python binary and will survive reboots.

### Applying code changes

The LaunchAgent runs a persistent process — file changes are not picked up automatically. After editing any code, restart the service:

```bash
launchctl kickstart -k gui/$(id -u)/com.yourname.meeting-presence
```

## Light colors

| Teams status | Color |
|---|---|
| Available | Green |
| Busy | Red |
| DoNotDisturb | Red-purple |
| Away / BeRightBack | Orange-red |
| Offline / Unknown | Off |

## Testing colors

Use `test_color.py` to preview a color on the Blynclight without restarting the service. Stop the service first so it doesn't hold the device:

```bash
launchctl bootout gui/$(id -u) ~/Library/LaunchAgents/com.yourname.meeting-presence.plist
.venv/bin/python test_color.py FF4500
```

Pass any hex color as the argument. When you've found a color you like, update `effects/blynclight.py` and restart the service.

## Adding more effects

The `effects/` directory supports multiple output devices. Each effect implements the `StatusEffect` base class:

```python
from effects.base import StatusEffect
from presence.base import PresenceStatus

class MyEffect(StatusEffect):
    def apply(self, status: PresenceStatus) -> None:
        # update your device here

    def on_unavailable(self) -> None:
        # called when Teams isn't running
```

Add it to the `effects` list in `main.py` and it will receive every status change alongside the Blynclight.

Planned: RGB wifi bulb support.
