from pathlib import Path
from datetime import timedelta

from nonebot import require, on_command

require("nonebot_plugin_argot")
require("nonebot_plugin_alconna")

from nonebot_plugin_alconna import Command
from nonebot_plugin_alconna.uniseg import Text, Image, UniMessage

from nonebot_plugin_argot import Argot, add_argot, get_message_id

cmd1 = Command("test1").build(use_cmd_start=True)


@cmd1.handle()
async def _():

    await UniMessage.text("This is a text message. Reply /background to get background image.").finish(
        argot={
            "name": "background",
            "segment": Image(url="https://koishi.chat/logo.png"),
            "expire": 240,  # The argot will expired after 4 minutes.
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

    await UniMessage(
        [
            Text("This is a text message. Reply /image to get image."),
            Argot("image", [Text("image"), Image(path=path)]),
        ]
    ).send()
