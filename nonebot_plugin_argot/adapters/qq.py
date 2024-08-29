from typing import Any
from contextlib import suppress

from nonebot.adapters import Bot as BaseBot
from nonebot.exception import MockApiException

from .utils import add_argot_from_hook

with suppress(ImportError):
    from nonebot.adapters.qq import Bot
    from nonebot.adapters.qq.models import Message as GuildMessage
    from nonebot.adapters.qq.models import PostC2CMessagesReturn, PostGroupMessagesReturn

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

        if "argot" not in data:
            return

        if not (msg_id := result.id):
            return

        await add_argot_from_hook(
            message_id=msg_id,
            argot_data=data["argot"],
        )

        raise MockApiException(result=result)
