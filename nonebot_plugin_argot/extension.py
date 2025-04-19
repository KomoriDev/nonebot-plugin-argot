from typing import Any

from nonebot.exception import MockApiException
from nonebot_plugin_alconna.uniseg import UniMessage
from nonebot_plugin_alconna.extension import Extension
from nonebot.internal.adapter import Bot, Event, Message
from nonebot_plugin_alconna.uniseg.message import SendWrapper as BaseSendWrapper
from nonebot_plugin_alconna.uniseg.message import current_send_wrapper as current_send_wrapper

from .segment import Argot
from .utils import get_message_id
from .data_source import add_argot_from_hook

argot_data = []
send_msg_apis = ["send", "post", "create", "im/v1/messages", "im/v1/images"]


def process_argot_message(send: str | Message | UniMessage) -> str | Message | UniMessage:
    if not isinstance(send, UniMessage):
        return send

    argot_segments = [seg for seg in send if isinstance(seg, Argot)]
    for segment in argot_segments:
        argot_data.append(segment.dump())

    return send.exclude(Argot) if argot_segments else send


class ArgotSendWrapper(BaseSendWrapper):
    async def __call__(self, bot: Bot, event: Event, send: str | Message | UniMessage):
        return process_argot_message(send)


class ArgotExtension(Extension):
    @property
    def priority(self) -> int:
        return 15

    @property
    def id(self) -> str:
        return "ArgotExtension"

    async def send_wrapper(self, bot: Bot, event: Event, send: str | Message | UniMessage):
        return process_argot_message(send)


@Bot.on_called_api
async def _(
    bot: Bot,
    exception: Exception | None,
    api: str,
    data: dict[str, Any],
    result: dict[str, Any] | bool,
) -> None:
    if not set(api.split("_")).intersection(send_msg_apis):
        return

    if exception or not result:
        return

    if not isinstance(result, dict):
        return

    if "argot" in data:
        if isinstance(data["argot"], list):
            for item in data["argot"]:
                argot_data.append(item)
        elif isinstance(data["argot"], dict):
            argot_data.append(data["argot"])
        else:
            raise ValueError(f"'argot' field must be a list or dict, got {type(data['argot']).__name__} instead.")

    if not argot_data:
        return

    message_id = get_message_id(result)
    if message_id is None:
        return

    await add_argot_from_hook(message_id, argot_data)
    argot_data.clear()

    raise MockApiException(result=result)
