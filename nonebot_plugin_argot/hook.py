from nonebot import get_driver
from nonebot.log import logger
from nonebot_plugin_alconna import command_manager

from . import adapters as adapters

driver = get_driver()


@driver.on_startup
async def _() -> None:
    command_manager.load_cache()
    logger.info("Argot cache loaded")


@driver.on_shutdown
async def _() -> None:
    command_manager.dump_cache()
    logger.info("Argot cache dumped")
