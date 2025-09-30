from typing import Any
from datetime import datetime, timedelta

from nonebot_plugin_alconna.uniseg import Receipt

message_id_keyword = ["message_id", "msgId", "id"]


def calculate_expired_at(expire_time: timedelta | int) -> datetime:
    """计算过期时间点"""
    create_at = datetime.now()
    if isinstance(expire_time, int):
        expire_time = timedelta(seconds=expire_time)

    expired_at = create_at + expire_time
    return expired_at


def get_message_id(message: Any) -> str | None:
    if isinstance(message, Receipt):
        message = message.msg_ids[0]

    return next(
        (message.get(key) for key in message_id_keyword if key in message),
    )
