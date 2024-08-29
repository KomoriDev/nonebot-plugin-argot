from typing import Any, cast
from contextlib import suppress

from nonebot.adapters import Bot as BaseBot
from nonebot.exception import MockApiException

from .utils import add_argot_from_hook

with suppress(ImportError):
    from nonebot.adapters.satori import Bot
    from nonebot.adapters.satori.models import MessageObject

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

        if api not in ["message_create"]:
            return

        if "argot" not in data:
            return

        if not isinstance(result, list) or not all(isinstance(res, MessageObject) for res in result):
            return

        result_messages = cast(list[MessageObject], result)
        result_message = result_messages[0]

        await add_argot_from_hook(
            message_id=result_message.id,
            argot_data=data["argot"],
        )

        raise MockApiException(result=result)
