from nonebot import require
from nonebot.plugin import PluginMetadata, inherit_supported_adapters

require("nonebot_plugin_alconna")
require("nonebot_plugin_localstore")
require("nonebot_plugin_apscheduler")
from nonebot_plugin_apscheduler import scheduler
from nonebot_plugin_alconna.uniseg.segment import At as At
from nonebot_plugin_alconna.uniseg.segment import I18n as I18n
from nonebot_plugin_alconna.uniseg.segment import Text as Text
from nonebot_plugin_alconna.uniseg.segment import AtAll as AtAll
from nonebot_plugin_alconna.uniseg.segment import Audio as Audio
from nonebot_plugin_alconna.uniseg.segment import Emoji as Emoji
from nonebot_plugin_alconna.uniseg.segment import Image as Image
from nonebot_plugin_alconna.uniseg.segment import Media as Media
from nonebot_plugin_alconna.uniseg.segment import Reply as Reply
from nonebot_plugin_alconna.uniseg.segment import Video as Video
from nonebot_plugin_alconna.uniseg.segment import Voice as Voice

from . import hook as hook
from . import matcher as matcher
from .segment import Argot as Argot
from .event import on_argot as on_argot
from .event import ArgotEvent as ArgotEvent
from .data_source import delete_expired_argots
from .data_source import add_argot as add_argot
from .utils import get_message_id as get_message_id
from .extension import ArgotExtension as ArgotExtension
from .extension import ArgotSendWrapper as ArgotSendWrapper
from .extension import current_send_wrapper as current_send_wrapper

__plugin_meta__ = PluginMetadata(
    name="暗语消息",
    description="为消息添加暗语支持",
    usage="详见文档",
    type="library",
    config=None,
    homepage="https://github.com/KomoriDev/nonebot-plugin-argot",
    supported_adapters=inherit_supported_adapters("nonebot_plugin_alconna"),
    extra={
        "unique_name": "Argot",
        "author": "Komorebi <mute231010@gmail.com>",
        "version": "0.2.2",
    },
)


@scheduler.scheduled_job("cron", hour="*/4", id="delete_expired_argots")
async def run_every_2_hour():
    await delete_expired_argots()
