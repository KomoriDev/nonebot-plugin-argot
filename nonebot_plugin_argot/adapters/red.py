from typing import Any
from contextlib import suppress

from nonebot.adapters import Bot as BaseBot
from nonebot.exception import MockApiException
from nonebot.compat import type_validate_python

from .utils import add_argot_from_hook

with suppress(ImportError):
    from nonebot.adapters.red import Bot
    from nonebot.adapters.red.api.model import Message as MessageModel

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

        if api not in ["send_message"]:
            return

        if "argot" not in data:
            return

        try:
            message = type_validate_python(MessageModel, result)
        except Exception:
            return

        await add_argot_from_hook(
            message_id=message.msgId,
            argot_data=data["argot"],
        )

        raise MockApiException(result=result)
