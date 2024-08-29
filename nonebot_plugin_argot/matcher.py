from nonebot.adapters import Bot, Event
from nonebot_plugin_alconna import Match, Arparma, Command
from nonebot_plugin_alconna.uniseg import Image, MsgId, UniMessage
from nonebot_plugin_alconna.builtins.extensions import ReplyRecordExtension

from .config import plugin_config
from .model import get_argot, get_argots
from .utils import is_data_url, extract_urls, format_argots, base64_to_bytes

argot_cmd = Command("argot [name:str]").build(
    block=True,
    use_cmd_start=True,
    extensions=[ReplyRecordExtension()],
    auto_send_output=True,
)


@argot_cmd.handle()
async def _(
    name: Match[str],
    msg_id: MsgId,
    bot: Bot,
    event: Event,
    command: Arparma,
    ext: ReplyRecordExtension,
):

    if "argot" in command.header_match.origin and event.get_user_id() not in bot.config.superusers:
        await UniMessage.text("指令 Argot 仅允许 SUPERUSER 使用").finish()

    if reply := ext.get_reply(msg_id):
        if name.available:
            argot = await get_argot(name.result, reply.id)
            if argot is None:
                await UniMessage.text("该暗语不存在或已过期").finish(at_sender=True)
            else:
                message = argot.content
                if is_data_url(message):
                    message = Image(raw=base64_to_bytes(message))
                else:
                    if plugin_config.url_to_image:
                        urls = extract_urls(message)
                        for url in urls:
                            message += Image(url=url)
                await UniMessage(message).finish(at_sender=True)

        argots = await get_argots(reply.id)
        if argots is None:
            await UniMessage.text("该消息没有设置暗语或已过期").finish(at_sender=True)
        message = format_argots(argots)
        await UniMessage.text(message).finish(reply_to=reply.id)
    else:
        await UniMessage.text("需回复一条消息").finish()
