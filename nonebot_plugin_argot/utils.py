import re
import base64
import binascii
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


def is_data_url(s: str) -> bool:
    data_url_pattern = re.compile(r"^data:(?P<mediatype>[\w+/]+)?(?P<base64>;base64)?,(?P<data>.*)$", re.DOTALL)

    match = data_url_pattern.match(s)
    if not match:
        return False

    if match.group("base64"):
        data = match.group("data")
        if len(data) % 4 != 0:
            return False
        try:
            base64.b64decode(data)
        except Exception:
            return False

    return True


def format_argots(argots: Sequence["Argot"]) -> str:
    formatted_text = "Argot\n"

    for argot in argots:
        name = argot.name
        content = argot.content if not is_data_url(argot.content) else "..."
        expired_at = argot.expired_at.strftime("%Y-%m-%d %H:%M:%S") if argot.expired_at else "Never"
        formatted_text += f"  - {name}: {content} (expired at: {expired_at})\n"
    return formatted_text


def extract_urls(message) -> list[str]:
    return re.findall(r"https?://[^\s]+", message)


def base64_to_bytes(base64_string: str) -> bytes:
    try:
        if "," in base64_string:
            base64_data = base64_string.split(",")[1]
        else:
            base64_data = base64_string

        missing_padding = len(base64_data) % 4
        if missing_padding:
            base64_data += "=" * (4 - missing_padding)

        return base64.b64decode(base64_data)

    except binascii.Error as e:
        raise ValueError(f"解码 Base64 字符串时出错: {e}")
