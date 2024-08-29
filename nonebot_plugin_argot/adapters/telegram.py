from typing import Any
from contextlib import suppress

from pydantic import ValidationError
from nonebot.adapters import Bot as BaseBot
from nonebot.exception import MockApiException
from nonebot.compat import type_validate_python

from .utils import add_argot_from_hook

with suppress(ImportError):
    from nonebot.adapters.telegram import Bot
    from nonebot.adapters.telegram.model import Message as TGMessage

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

        if api in [
            "send_message",
            "send_photo",
            "send_audio",
            "send_document",
            "send_video",
            "send_animation",
            "send_voice",
            "send_video_note",
            "send_location",
            "send_venue",
            "send_contact",
            "send_poll",
            "send_dice",
            "send_sticker",
            "send_invoice",
        ]:
            try:
                tg_message = type_validate_python(TGMessage, result)
            except ValidationError:
                return
            message_id = str(tg_message.message_id)

        elif api == "send_media_group":
            try:
                tg_messages = [type_validate_python(TGMessage, res) for res in result]
            except ValidationError:
                return
            tg_message = tg_messages[0]
            message_id = str(tg_message.message_id)

        else:
            return

        if "argot" not in data:
            return

        await add_argot_from_hook(
            message_id=message_id,
            argot_data=data["argot"],
        )

        raise MockApiException(result=result)
