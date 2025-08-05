from datetime import datetime
from typing import Any, Literal
from dataclasses import field, dataclass

from nonebot_plugin_alconna.uniseg.segment import Text, Media, Segment


@dataclass
class Argot:
    message_id: str
    name: str
    segment: str | Segment | list[Segment] | None = None
    command: str | Literal[False] | None = None
    created_at: datetime = field(default=datetime.now(), init=False)
    expired_at: datetime | None = field(default=None)
    extra: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        self.message_id = str(self.message_id)
        self.command = self.name if self.command is None else self.command
        self.expired_at = (
            datetime.fromisoformat(self.expired_at) if isinstance(self.expired_at, str) else self.expired_at
        )

        if self.segment is None:
            return
        segment = []
        self.segment = (
            [Text(self.segment)]
            if isinstance(self.segment, str)
            else [self.segment] if isinstance(self.segment, Segment) else self.segment
        )

        for seg in self.segment:
            if issubclass(type(seg), Segment):
                if isinstance(seg, Media) and seg.path:
                    seg.path = str(seg.path)
                segment.append(seg.dump())
            else:
                segment.append(seg)
        self.segment = segment

    def dump(self) -> dict[str, Any]:
        return {
            "message_id": self.message_id,
            "name": self.name,
            "segment": list(self.segment) if self.segment else None,  # type: ignore
            "command": self.command,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "expired_at": self.expired_at.isoformat() if self.expired_at else None,
            "extra": self.extra if self.extra else {},
        }

    def dump_segment(self) -> str | list | None:
        if self.segment is None:
            return None

        if isinstance(self.segment, str):
            return self.segment
        elif isinstance(self.segment, Segment):
            return [self.segment.dump()]
        return list(self.segment)
