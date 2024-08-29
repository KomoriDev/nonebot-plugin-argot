from typing import Any
from contextlib import suppress

from nonebot.adapters import Bot as BaseBot
from nonebot.exception import MockApiException

from .utils import add_argot_from_hook

with suppress(ImportError):
    from nonebot.adapters.dodo import Bot
    from nonebot.adapters.dodo.models import MessageReturn

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

        if api not in ["set_channel_message_send", "set_personal_message_send"]:
            return

        if "argot" not in data:
            return

        if not isinstance(result, MessageReturn):
            return

        await add_argot_from_hook(
            message_id=result.message_id,
            argot_data=data["argot"],
        )

        raise MockApiException(result=result)
