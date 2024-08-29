from typing import Any

from nonebot import get_driver
from nonebot.log import logger
from nonebot.adapters import Bot
from nonebot.exception import MockApiException
from nonebot_plugin_alconna import command_manager

from .model import add_argot

driver = get_driver()


@driver.on_startup
async def _() -> None:
    command_manager.load_cache()
    logger.info("Argot cache loaded")


@driver.on_shutdown
async def _() -> None:
    command_manager.dump_cache()
    logger.info("Argot cache dumped")


@Bot.on_called_api
async def _(
    bot: Bot,
    exception: Exception | None,
    api: str,
    data: dict[str, Any],
    result: dict[str, Any],
) -> None:
    if not isinstance(bot, Bot):
        return

    if exception or not result:
        return

    if "send_" not in api or "argot" not in data:
        return

    argot_name: str = data["argot"].get("name")
    argot_content: str = data["argot"].get("content")
    argot_command: str = data["argot"].get("command", None)
    argot_expired: int = data["argot"].get("expire", None)

    message_id = str(result["message_id"])

    await add_argot(
        name=argot_name,
        message_id=message_id,
        content=argot_content,
        command=argot_command,
        expire_time=argot_expired,
    )

    raise MockApiException(result=result)
