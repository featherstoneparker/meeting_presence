import json
import socket

from presence.base import PresenceStatus
from effects.base import StatusEffect

_GOVEE_COMMAND_PORT = 4003
_GOVEE_DISCOVERY_PORT = 4001
_GOVEE_MULTICAST_ADDR = "239.255.255.250"
_SOCKET_TIMEOUT = 2

_COLORS = {
    "Available":       (0,   255, 0),
    "Busy":            (255, 0,   0),
    "DoNotDisturb":    (255, 0,   128),
    "Away":            (255, 69,  0),
    "BeRightBack":     (255, 69,  0),
    "Offline":         (0,   0,   0),
    "PresenceUnknown": (0,   0,   0),
}
_DEFAULT_COLOR = (128, 128, 128)


def discover_govee_devices(timeout: float = 3.0) -> list[dict]:
    """Scan the local network for Govee LAN-enabled devices."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
    sock.settimeout(timeout)

    msg = json.dumps({"msg": {"cmd": "scan", "data": {"account_topic": "reserve"}}})
    sock.sendto(msg.encode(), (_GOVEE_MULTICAST_ADDR, _GOVEE_DISCOVERY_PORT))

    devices = []
    try:
        while True:
            data, addr = sock.recvfrom(1024)
            payload = json.loads(data.decode())
            if payload.get("msg", {}).get("cmd") == "scan":
                devices.append({"ip": addr[0], **payload["msg"]["data"]})
    except socket.timeout:
        pass
    finally:
        sock.close()

    return devices


def _send_command(ip: str, command: dict) -> None:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(_SOCKET_TIMEOUT)
    try:
        msg = json.dumps({"msg": command})
        sock.sendto(msg.encode(), (ip, _GOVEE_COMMAND_PORT))
    finally:
        sock.close()


class GoveeLanEffect(StatusEffect):
    def __init__(self, ip: str, brightness: int = 100) -> None:
        self._ip = ip
        self._brightness = brightness

    def apply(self, status: PresenceStatus) -> None:
        r, g, b = _COLORS.get(status.availability, _DEFAULT_COLOR)
        if (r, g, b) == (0, 0, 0):
            self._turn_off()
            return
        _send_command(self._ip, {"cmd": "turn", "data": {"value": 1}})
        _send_command(self._ip, {"cmd": "brightness", "data": {"value": self._brightness}})
        _send_command(self._ip, {"cmd": "colorwc", "data": {
            "color": {"r": r, "g": g, "b": b},
            "colorTemInKelvin": 0,
        }})

    def on_unavailable(self) -> None:
        self._turn_off()

    def _turn_off(self) -> None:
        _send_command(self._ip, {"cmd": "turn", "data": {"value": 0}})
