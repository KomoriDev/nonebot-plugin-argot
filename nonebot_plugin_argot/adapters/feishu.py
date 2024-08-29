import re
from typing import Any
from contextlib import suppress

from nonebot.adapters import Bot as BaseBot
from nonebot.exception import MockApiException

from .utils import add_argot_from_hook

with suppress(ImportError):
    from nonebot.adapters.feishu import Bot

    @Bot.on_called_api
    async def _(
        bot: BaseBot,
        exception: Exception | None,
        api: str,
        data: dict[str, Any],
        result: dict[str, Any],
    ) -> None:
        if not isinstance(bot, Bot):
            return

        if exception or not result:
            return

        if api not in ["im/v1/messages"] and not re.fullmatch(r"im/v1/messages/\S+/reply", api):
            return

        if "argot" not in data or "data" not in result:
            return

        await add_argot_from_hook(
            message_id=result["data"]["message_id"],
            argot_data=data["argot"],
        )

        raise MockApiException(result=result)
