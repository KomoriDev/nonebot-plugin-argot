from typing import Any
from contextlib import suppress

from nonebot.adapters import Bot as BaseBot
from nonebot.exception import MockApiException

from .utils import add_argot_from_hook

with suppress(ImportError):
    from nonebot.adapters.qq import Bot
    from nonebot.adapters.qq.models import Message as GuildMessage
    from nonebot.adapters.qq.models import PostC2CMessagesReturn, PostGroupMessagesReturn

    segments_dict = {}

    @Bot.on_calling_api
    async def _(
        bot: BaseBot,
        api: str,
        data: dict[str, Any],
    ) -> None:
        if not isinstance(bot, Bot):
            return

        if api not in ["post_messages", "post_dms_messages", "post_c2c_messages", "post_group_messages"]:
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

        if api == "post_messages":
            if not isinstance(result, GuildMessage):
                return
        elif api == "post_dms_messages":
            if not isinstance(result, GuildMessage):
                return
        elif api == "post_c2c_messages":
            if not isinstance(result, PostC2CMessagesReturn):
                return
        elif api == "post_group_messages":
            if not isinstance(result, PostGroupMessagesReturn):
                return
        else:
            return

        if not (msg_id := result.id):
            return

        if not segments_dict:
            return

        await add_argot_from_hook(msg_id, segments_dict)
        segments_dict.clear()

        raise MockApiException(result=result)
