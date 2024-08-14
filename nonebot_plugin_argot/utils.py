import re
from typing import TYPE_CHECKING
from collections.abc import Sequence
from datetime import datetime, timedelta

if TYPE_CHECKING:
    from .model import Argot


def calculate_expired_at(expire_time: timedelta | int) -> datetime:
    """计算过期时间点"""
    create_at = datetime.now()
    if isinstance(expire_time, int):
        expire_time = timedelta(seconds=expire_time)

    expired_at = create_at + expire_time
    return expired_at


def format_argots(argots: Sequence["Argot"]) -> str:
    formatted_text = "Argot\n"

    for argot in argots:
        name = argot.name
        content = argot.content
        expired_at = argot.expired_at.strftime("%Y-%m-%d %H:%M:%S") if argot.expired_at else "Never"
        formatted_text += f"  - {name}: {content} (expired at: {expired_at})\n"
    return formatted_text


def extract_urls(message) -> list[str]:
    return re.findall(r"https?://[^\s]+", message)
