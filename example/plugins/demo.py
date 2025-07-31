from pathlib import Path
from datetime import timedelta

from nonebot import require, on_command

require("nonebot_plugin_argot")
require("nonebot_plugin_alconna")
require("nonebot_plugin_waiter")

from nonebot_plugin_alconna import Command
from nonebot_plugin_alconna.uniseg import UniMessage
from nonebot_plugin_waiter import prompt

from nonebot_plugin_argot.extension import ArgotExtension, ArgotSendWrapper, current_send_wrapper
from nonebot_plugin_argot import Text, Argot, Image, ArgotEvent, on_argot, add_argot, get_message_id

cmd1 = Command("test1").build(use_cmd_start=True)


@cmd1.handle()
async def _():

    await UniMessage.text("This is a text message. Reply /background to get background image.").finish(
        argot={
            "name": "background",
            "segment": Image(url="https://koishi.chat/logo.png"),
            "expired_at": 240,  # The argot will expired after 4 minutes.
        }
    )


cmd2 = on_command("test2")


@cmd2.handle()
async def _():
    message = await cmd2.send("This is a text message. Reply /background to get background image.")
    await add_argot(
        message_id=get_message_id(message) or "",
        name="background",
        segment=Image(url="https://koishi.chat/logo.png"),
        expired_at=timedelta(minutes=2),
    )


cmd3 = Command("test3").build(use_cmd_start=True)


@cmd3.handle()
async def _():

    path: Path = Path(__file__).parent / "image.png"

    with current_send_wrapper.use(ArgotSendWrapper()):
        await UniMessage(
            [
                Text("This is a text message. Reply /image to get image."),
                Argot("image", [Text("image"), Image(path=path)]),
            ]
        ).send()


cmd4 = Command("test4").build(use_cmd_start=True, extensions=[ArgotExtension()])


@cmd4.handle()
async def _():

    path: Path = Path(__file__).parent / "image.png"

    await UniMessage(
        [
            Text("This is a text message. Reply /image to get image."),
            Argot("image", [Text("image"), Image(path=path)]),
        ]
    ).send()


cmd5 = Command("test5").build(use_cmd_start=True, extensions=[ArgotExtension()])


@cmd5.handle()
async def _():

    await UniMessage(
        [
            Text("This is a text message. Reply /target to get raw data."),
            Argot("target"),
        ]
    ).send()


@on_argot("target")
async def _(event: ArgotEvent):
    await event.target.send(f"触发暗语：{event.name}")
    await event.target.send(f"发送对象：{event.target.dump()}")


cmd6 = Command("test6").build(use_cmd_start=True, extensions=[ArgotExtension()])


@cmd6.handle()
async def _():

    await UniMessage(
        [
            Text("This is a continuous interactive message. Reply /continue to trigger the action."),
            Argot("cmd6_continue", extra={"id": 114514, "status": "success"}, command="continue"),
        ]
    ).send()


@on_argot("cmd6_continue")
async def _(event: ArgotEvent):
    await event.target.send(f"初始状态：{event.extra['status']}；\n触发暗语事件：{repr(event)}")
    resp = await prompt("请输入XXX", timeout=60)
    if resp is None:
        await event.target.send("等待超时！")
        return
    await event.target.send(f"你输入了{resp}")
