from typing import Any
from contextlib import suppress

from nonebot.adapters import Bot as BaseBot
from nonebot.exception import MockApiException

from .utils import add_argot_from_hook

with suppress(ImportError):
    from nonebot.adapters.kaiheila import Bot
    from nonebot.adapters.kaiheila.api.model import MessageCreateReturn

    segments_dict = {}

    @Bot.on_calling_api
    async def _(
        bot: BaseBot,
        api: str,
        data: dict[str, Any],
    ) -> None:
        if not isinstance(bot, Bot):
            return

        if api not in ["message_create", "directMessage_create"]:
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
        result: Any,
    ) -> None:
        if not isinstance(bot, Bot):
            return

        if exception or not result:
            return

        if not isinstance(result, MessageCreateReturn) or not (msg_id := result.msg_id):
            return

        if not segments_dict:
            return

        await add_argot_from_hook(msg_id, segments_dict)
        segments_dict.clear()

        raise MockApiException(result=result)
