from datetime import timedelta
from typing import Any, Literal
from typing_extensions import Self, override

from nonebot.adapters import Message as BaseMessage
from nonebot_plugin_alconna.uniseg import Text, Segment
from nonebot.adapters import MessageSegment as BaseMessageSegment


class MessageSegment(BaseMessageSegment["Message"]):

    @classmethod
    @override
    def get_message_class(cls) -> type["Message"]:
        return Message

    @override
    def __str__(self) -> str:
        return "[argot]"

    @override
    def is_text(self) -> bool:
        return False

    @classmethod
    def argot(
        cls,
        name: str,
        segment: str | Segment | list[Segment],
        command: str | Literal[False] | None = None,
        expired_at: timedelta | None = None,
        extra: dict[str, Any] = {},
    ) -> Self:
        seg = (
            [Text(segment).dump()]
            if isinstance(segment, str)
            else [segment.dump()] if isinstance(segment, Segment) else [seg.dump() for seg in segment]
        )
        return cls(
            "argot",
            {
                "name": name,
                "segment": seg,
                "command": command,
                "expired_at": expired_at,
                "extra": extra,
            },
        )


class Message(BaseMessage[MessageSegment]):

    @classmethod
    @override
    def get_segment_class(cls) -> type[MessageSegment]:
        return MessageSegment
