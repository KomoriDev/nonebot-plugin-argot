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

    segments_dict = {}

    @Bot.on_calling_api
    async def _(
        bot: BaseBot,
        api: str,
        data: dict[str, Any],
    ) -> None:
        if not isinstance(bot, Bot):
            return

        if api not in [
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
            "send_media_group",
        ]:
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

        if not segments_dict:
            return

        await add_argot_from_hook(message_id, segments_dict)
        segments_dict.clear()

        raise MockApiException(result=result)
