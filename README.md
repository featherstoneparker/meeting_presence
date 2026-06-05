# meeting_presence

Reads your Microsoft Teams presence status from local log files and drives an Embrava Blynclight USB status light. No cloud auth required — works entirely offline by parsing Teams' local logs.

## How it works

Teams writes presence changes (Available, Busy, DoNotDisturb, etc.) to a local log file in real time. This script tails that log every 5 seconds and updates the light color accordingly.

## Requirements

- macOS
- Microsoft Teams (new Teams 2.0)
- Embrava Blynclight connected via USB
- Python 3.9+

## Setup

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

### macOS permissions

The first time you run it, macOS will ask if your terminal app can access data from other apps. Click **Allow**. If you plan to run this from cron or a background process, grant **Full Disk Access** to the Python binary in **System Settings → Privacy & Security → Full Disk Access**.

The Python binary to add is:
```
/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/bin/python3.9
```

## Usage

```bash
.venv/bin/python main.py
```

The script runs as a loop, printing status changes and updating the light. Press `Ctrl+C` to stop.

## Light colors

| Teams status | Color |
|---|---|
| Available | Green |
| Busy | Red |
| DoNotDisturb | Red-purple |
| Away / BeRightBack | Orange |
| Offline / Unknown | Off |

## Adding more effects

The `effects/` directory is designed to support multiple output devices. Each effect implements the `StatusEffect` base class:

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
