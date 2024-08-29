from typing import Any
from contextlib import suppress

from nonebot.adapters import Bot as BaseBot
from nonebot.exception import MockApiException

from .utils import add_argot_from_hook

with suppress(ImportError):
    from nonebot.adapters.kaiheila import Bot
    from nonebot.adapters.kaiheila.api.model import MessageCreateReturn

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

        if api not in ["message_create", "directMessage_create"]:
            return

        if "argot" not in data:
            return

        if not isinstance(result, MessageCreateReturn) or not (msg_id := result.msg_id):
            return

        await add_argot_from_hook(
            message_id=msg_id,
            argot_data=data["argot"],
        )

        raise MockApiException(result=result)
