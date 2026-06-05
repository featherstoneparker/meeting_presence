from blynclight import BlyncLight

from presence.base import PresenceStatus
from effects.base import StatusEffect

# RGB tuples for each availability state
_COLORS = {
    "Available":      (0,   255, 0),    # green
    "Busy":           (255, 0,   0),    # red
    "DoNotDisturb":   (255, 0,   128),  # red-purple
    "Away":           (255, 165, 0),    # orange
    "BeRightBack":    (255, 165, 0),    # orange
    "Offline":        (0,   0,   0),    # off
    "PresenceUnknown":(0,   0,   0),    # off
}
_DEFAULT_COLOR = (128, 128, 128)  # dim white for unknown states


class BlynclightEffect(StatusEffect):
    def __init__(self) -> None:
        try:
            self._light = BlyncLight.get_light()
        except Exception as e:
            raise RuntimeError(
                "Could not open Blynclight. If the Embrava app is running, quit it first."
            ) from e

    def apply(self, status: PresenceStatus) -> None:
        r, g, b = _COLORS.get(status.availability, _DEFAULT_COLOR)
        with self._light.updates_paused():
            self._light.red = r
            self._light.green = g
            self._light.blue = b
            self._light.on = 1

    def on_unavailable(self) -> None:
        with self._light.updates_paused():
            self._light.red = 0
            self._light.green = 0
            self._light.blue = 0
            self._light.on = 0
