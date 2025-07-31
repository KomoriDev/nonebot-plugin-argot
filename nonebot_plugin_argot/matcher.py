import arclet.letoderea as le
from nonebot.adapters import Bot, Event
from nonebot_plugin_alconna import Match, Arparma, Command
from nonebot_plugin_alconna.uniseg import MsgId, UniMessage, get_target
from nonebot_plugin_alconna.builtins.extensions import ReplyRecordExtension

from .hook import driver
from .event import ArgotEvent
from .data_source import get_argot, get_argots

config = driver.config

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
                await UniMessage.text("该暗语不存在或已过期").finish(reply_to=reply.id)
            else:
                target = get_target(event, bot)
                await le.publish(ArgotEvent(name=argot.name, data=argot, target=target, extra=argot.extra))
                if data := argot.dump_segment():
                    await UniMessage.load(data).finish()
                await argot_cmd.finish()

        argots = await get_argots(reply.id)
        messages = []

        if argots is None:
            await UniMessage.text("该消息没有设置暗语或已过期").finish(reply_to=reply.id)

        for idx, argot in enumerate(argots, 1):
            message = f"▏暗语 #{idx}\n"
            message += f"✦ 名称：{argot.name}\n"

            create_time = argot.created_at.strftime("%Y-%m-%d %H:%M")
            message += f"✦ 创建：{create_time}\n"

            if argot.expired_at:
                expire_time = argot.expired_at.strftime("%Y-%m-%d %H:%M")
                message += f"✦ 过期：{expire_time}\n"
            else:
                message += "✦ 过期：永久有效\n"

            cmd = argot.command if isinstance(argot.command, str) else "未绑定命令"
            message += f"✦ 触发：{'|'.join(config.command_start)}{cmd}\n"

            if data := argot.dump_segment():
                message += f"✦ 内容：{UniMessage.load(data)}\n"
            else:
                message += "✦ 内容：未知\n"

            if argot.extra:
                message += f"✦ 额外参数：{repr(argot.extra)}\n"

            messages.append(message)
        await UniMessage.text(f"🔍 消息暗语查询（共 {len(argots)} 条）\n" + " ".join(messages)).finish(
            reply_to=reply.id
        )
    else:
        await UniMessage.text("需回复一条消息").finish()
