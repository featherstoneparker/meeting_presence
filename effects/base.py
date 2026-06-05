from abc import ABC, abstractmethod
from presence.base import PresenceStatus


class StatusEffect(ABC):
    @abstractmethod
    def apply(self, status: PresenceStatus) -> None:
        """Called whenever presence status changes."""
        ...

    def on_unavailable(self) -> None:
        """Called when presence can't be read (Teams not running, etc.)."""
        pass
