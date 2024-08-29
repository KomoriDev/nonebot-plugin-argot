from typing import Any
from contextlib import suppress

from nonebot.adapters import Bot as BaseBot
from nonebot.exception import MockApiException

from .utils import add_argot_from_hook

with suppress(ImportError):
    from nonebot.adapters.discord import Bot
    from nonebot.adapters.discord.api import MessageGet

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

        if api not in ["create_message"]:
            return

        if "argot" not in data:
            return

        if not isinstance(result, MessageGet):
            return

        await add_argot_from_hook(
            message_id=str(result.id),
            argot_data=data["argot"],
        )

        raise MockApiException(result=result)
