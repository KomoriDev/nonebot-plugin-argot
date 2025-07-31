import json
import asyncio
from functools import wraps
from typing import Any, Literal
from datetime import datetime, timedelta

import aiofiles
from nonebot_plugin_alconna.uniseg.segment import Segment
from nonebot_plugin_localstore import get_plugin_data_file

from .typing import Argot
from .utils import calculate_expired_at

JSON_FILE = get_plugin_data_file("argot.json")
lock = asyncio.Lock()

if not JSON_FILE.exists():
    if not JSON_FILE.exists():
        JSON_FILE.write_text(json.dumps([], ensure_ascii=False, indent=2))


async def load_data() -> list[Argot]:
    async with lock:
        async with aiofiles.open(JSON_FILE, encoding="utf-8") as f:
            content = await f.read()
            data = [
                Argot(**{k: v for k, v in data.items() if k not in {"created_at"}})
                for data in json.loads(content)
                if data
            ]
            return data


async def save_data(data: list[Argot]) -> None:
    async with lock:
        to_save = []
        for item in data:
            to_save.append(item.dump())

        async with aiofiles.open(JSON_FILE, "w", encoding="utf-8") as f:
            await f.write(json.dumps(to_save, ensure_ascii=False, indent=2))


async def add_argot(
    message_id: str,
    name: str,
    segment: str | Segment | list[Segment] | None = None,
    command: str | Literal[False] | None = None,
    expired_at: timedelta | None = None,
    extra: dict[str, Any] = {},
) -> None:
    from .matcher import argot_cmd

    argot = Argot(
        message_id=message_id,
        name=name,
        segment=segment,
        command=command,
        expired_at=calculate_expired_at(expired_at) if expired_at else None,
        extra=extra,
    )

    if argot.command:
        argot_cmd.shortcut(argot.command, {"command": f"argot {argot.name}", "prefix": True, "fuzzy": False})

    data = await load_data()
    data = [item for item in data if not (item.message_id == argot.message_id and item.name == argot.name)]

    data.append(argot)

    await save_data(data)


async def add_argot_from_hook(
    message_id: str,
    argot_data: list[dict[str, Any]],
) -> None:
    for data in argot_data:
        name = data["name"]
        segment = data.get("segment", None)
        command = data.get("command", None)
        expired = data.get("expired_at", None)
        extra = data.get("extra", {})

        await add_argot(
            message_id=message_id,
            name=name,
            segment=segment,
            command=command,
            expired_at=expired,
            extra=extra,
        )


async def delete_expired_argots() -> None:
    now = datetime.now()
    data = await load_data()
    data = [item for item in data if item.expired_at is None or item.expired_at > now]
    await save_data(data)


def clean_expired_data(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        await delete_expired_argots()
        return await func(*args, **kwargs)

    return wrapper


@clean_expired_data
async def get_argot(name: str, message_id: str) -> Argot | None:
    data = await load_data()
    for item in data:
        if item.name == name and item.message_id == message_id:
            return item
    return None


@clean_expired_data
async def get_argots(message_id: str) -> list[Argot] | None:
    data = await load_data()
    filtered = [item for item in data if item.message_id == message_id]
    return filtered if filtered else None
