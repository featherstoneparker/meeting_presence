from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class PresenceStatus:
    platform: str
    availability: str  # Available, Busy, Away, DoNotDisturb, Offline, etc.
    activity: str      # InAMeeting, InACall, Focusing, etc.

    @property
    def is_in_meeting(self) -> bool:
        return self.activity in {"InAMeeting", "InACall", "InAConferenceCall", "Presenting"}

    @property
    def is_available(self) -> bool:
        return self.availability == "Available"

    def __str__(self) -> str:
        return f"[{self.platform}] {self.availability} / {self.activity}"


class PresenceProvider(ABC):
    @abstractmethod
    def get_status(self) -> PresenceStatus:
        ...
