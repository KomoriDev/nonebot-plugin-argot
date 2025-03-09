from typing import Any
from contextlib import suppress

from nonebot.adapters import Bot as BaseBot
from nonebot.exception import MockApiException

from .utils import add_argot_from_hook

with suppress(ImportError):
    from nonebot.adapters.onebot.v12 import Bot

    message_id = ""
    segments_dict = {}

    @Bot.on_calling_api
    async def _(
        bot: BaseBot,
        api: str,
        data: dict[str, Any],
    ) -> None:
        if not isinstance(bot, Bot):
            return

        if api not in ["send_message"]:
            return

        if "argot" in data:
            segments_dict.update(data["argot"])
            return

        if data.get("message") is None:
            return

        segments = [seg for seg in data["message"] if seg.type == "argot"]

        if not segments:
            return

        for seg in segments:
            segments_dict.update(seg.__dict__["data"])

        data["message"] = [seg for seg in data["message"] if seg.type != "argot"]

    @Bot.on_called_api
    async def _(
        bot: BaseBot,
        exception: Exception | None,
        api: str,
        data: dict[str, Any],
        result: dict[str, Any] | bool,
    ) -> None:
        if not isinstance(bot, Bot):
            return

        if not isinstance(result, dict):
            return

        if exception or not result:
            return

        if not segments_dict:
            return

        message_id = result.get("message_id")
        if message_id is None:
            return

        await add_argot_from_hook(str(message_id), segments_dict)
        segments_dict.clear()

        raise MockApiException(result=result)
