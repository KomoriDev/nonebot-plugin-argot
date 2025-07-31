from datetime import timedelta
from typing import Any, Literal
from dataclasses import field, dataclass

from nonebot.adapters import Bot, Message
from nonebot_plugin_alconna.uniseg.exporter import MessageExporter
from nonebot_plugin_alconna.uniseg.fallback import FallbackStrategy
from nonebot_plugin_alconna.uniseg.segment import Text, Media, Segment, custom_handler

from .message import MessageSegment


@dataclass
class Argot(Segment):
    name: str
    segment: str | Segment | list[Segment] | None = field(default=None)
    command: str | Literal[False] | None = field(default=None, kw_only=True)
    expired_at: int | timedelta = field(default_factory=timedelta, kw_only=True)
    extra: dict[str, Any] = field(default_factory=dict, kw_only=True)

    def __str__(self):
        return ""

    def __post_init__(self):
        self.segment = (
            [Text(self.segment)]
            if isinstance(self.segment, str)
            else [self.segment] if isinstance(self.segment, Segment) else self.segment
        )

        if self.segment is None:
            self.segment = []

        for seg in self.segment:
            if isinstance(seg, Media) and seg.path:
                seg.path = str(seg.path)

        if isinstance(self.expired_at, timedelta):
            self.expired_at = int(self.expired_at.total_seconds())

        self.command = self.name if self.command is None else self.command


@custom_handler(Argot)
async def argot_export(exporter: MessageExporter, seg: Argot, bot: Bot | None, fallback: bool | FallbackStrategy):
    if issubclass(exporter.get_message_type(), Message):
        return MessageSegment.argot(
            **{
                "name": seg.name,
                "segment": seg.segment,
                "command": seg.command,
                "expired_at": seg.expired_at,
                "extra": seg.extra,
            }
        )
    return None
