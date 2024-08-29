from nonebot import require
from nonebot.plugin import PluginMetadata, inherit_supported_adapters

require("nonebot_plugin_orm")
require("nonebot_plugin_alconna")
require("nonebot_plugin_apscheduler")
from nonebot_plugin_apscheduler import scheduler

from . import migrations
from . import hook as hook
from .config import Config
from . import matcher as matcher
from .model import delete_expired_argots
from .model import add_argot as add_argot
from .model import get_argot as get_argot
from .model import get_argots as get_argots

__plugin_meta__ = PluginMetadata(
    name="暗语消息",
    description="为消息添加暗语支持",
    usage="详见文档",
    type="library",
    config=Config,
    homepage="https://github.com/KomoriDev/nonebot-plugin-argot",
    supported_adapters=inherit_supported_adapters("nonebot_plugin_alconna"),
    extra={
        "unique_name": "Argot",
        "orm_version_location": migrations,
        "author": "Komorebi <mute231010@gmail.com>",
        "version": "0.1.4",
    },
)


@scheduler.scheduled_job("cron", hour="*/4", id="delete_expired_argots")
async def run_every_2_hour():
    await delete_expired_argots()
