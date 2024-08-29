from typing import Any

from ..model import add_argot


async def add_argot_from_hook(
    message_id: str,
    argot_data: dict[str, Any],
) -> None:
    name: str = argot_data["name"]
    content: str = argot_data["content"]
    command: str = argot_data.get("command", None)
    expired: int = argot_data.get("expire", None)

    await add_argot(
        name=name,
        message_id=message_id,
        content=content,
        command=command,
        expire_time=expired,
    )
