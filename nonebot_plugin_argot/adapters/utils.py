from typing import Any

from ..data_source import add_argot


async def add_argot_from_hook(
    message_id: str,
    argot_data: dict[str, Any],
) -> None:
    name = argot_data["name"]
    segment = argot_data["segment"]
    command = argot_data.get("command", None)
    expired = argot_data.get("expired_at", None)

    await add_argot(message_id=message_id, name=name, segment=segment, command=command, expired_at=expired)
