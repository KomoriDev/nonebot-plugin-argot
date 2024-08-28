from pathlib import Path
from datetime import timedelta

from nonebot import require, on_command

require("nonebot_plugin_argot")
require("nonebot_plugin_alconna")

from nonebot_plugin_alconna import Command
from nonebot_plugin_alconna.uniseg import UniMessage

from nonebot_plugin_argot import add_argot

from .utils import image_to_base64

cmd1 = Command("test1").build(use_cmd_start=True)


@cmd1.handle()
async def _():

    message = await UniMessage.text("This is a text message. Reply /background to get background image.").send(
        argot={
            "name": "background",
            "command": "background",
            "content": "https://koishi.chat/logo.png",
            "expire": 240,  # The argot will expired after 4 minutes.
        }
    )

    await add_argot(
        "author",
        message.msg_ids[0]["message_id"],
        content="某内鬼",
        expire_time=timedelta(minutes=2),  # use timedelta to set expire time
    )
    await cmd1.finish()


cmd2 = on_command("test2")


@cmd2.handle()
async def _():
    message = await cmd2.send("A text message.")
    await add_argot(
        "author",
        message["message_id"],
        content="某内鬼",
        expire_time=timedelta(minutes=2),
    )


cmd3 = Command("test3").build(use_cmd_start=True)


@cmd3.handle()
async def _():

    path: Path = Path(__file__).parent / "image.png"

    message = await UniMessage.text("This is a text message. Reply /image to get image.").send(
        argot={
            "name": "image",
            "command": "image",
            "content": image_to_base64(path),
            "expire": 240,  # The argot will expired after 4 minutes.
        }
    )

    await add_argot(
        "author",
        message.msg_ids[0]["message_id"],
        content="某内鬼",
        expire_time=timedelta(minutes=2),  # use timedelta to set expire time
    )
    await cmd1.finish()
