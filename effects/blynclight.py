from blynclight import BlyncLight

from presence.base import PresenceStatus
from effects.base import StatusEffect

# RGB tuples for each availability state
_COLORS = {
    "Available":      (0,   255, 0),    # green
    "Busy":           (255, 0,   0),    # red
    "DoNotDisturb":   (255, 0,   128),  # red-purple
    "Away":           (255, 69,  0),    # orange-red
    "BeRightBack":    (255, 69,  0),    # orange-red
    "Offline":        (0,   0,   0),    # off
    "PresenceUnknown":(0,   0,   0),    # off
}
_DEFAULT_COLOR = (128, 128, 128)  # dim white for unknown states


class BlynclightEffect(StatusEffect):
    def __init__(self) -> None:
        self._light = None

    def _get_light(self):
        if self._light is not None:
            return self._light
        try:
            self._light = BlyncLight.get_light()
        except Exception:
            self._light = None
        return self._light

    def apply(self, status: PresenceStatus) -> None:
        light = self._get_light()
        if light is None:
            return
        r, g, b = _COLORS.get(status.availability, _DEFAULT_COLOR)
        try:
            with light.updates_paused():
                light.red = r
                light.green = g
                light.blue = b
                light.on = 1
        except Exception:
            self._light = None  # device went away; retry next cycle

    def on_unavailable(self) -> None:
        light = self._get_light()
        if light is None:
            return
        try:
            with light.updates_paused():
                light.red = 0
                light.green = 0
                light.blue = 0
                light.on = 0
        except Exception:
            self._light = None
