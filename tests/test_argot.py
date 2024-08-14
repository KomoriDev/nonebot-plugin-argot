from nonebug import App
from nonebot import get_adapter
from nonebot.adapters.onebot.v11 import Bot as OneBotV11Bot
from nonebot.adapters.onebot.v11 import Adapter as OneBotV11Adapter
from nonebot.adapters.onebot.v11 import Message as OneBotV11Message

from .utils import fake_v11_group_message_event


async def test_send_argot(app: App):
    from nonebot import on_command

    matcher = on_command("test")

    @matcher.handle()
    async def _():
        await matcher.finish("A normal message", argot={"name": "test", "content": "A argot message"})

    async with app.test_matcher(matcher) as ctx:
        adapter = get_adapter(OneBotV11Adapter)
        bot = ctx.create_bot(base=OneBotV11Bot, adapter=adapter)
        event = fake_v11_group_message_event(message=OneBotV11Message("/test"))

        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "A normal message", argot={"name": "test", "content": "A argot message"})
        ctx.should_finished()


async def test_superuser_get_argot_without_reply(app: App):
    from nonebot_plugin_argot.matcher import argot_cmd

    async with app.test_matcher(argot_cmd) as ctx:
        adapter = get_adapter(OneBotV11Adapter)
        bot = ctx.create_bot(base=OneBotV11Bot, adapter=adapter)
        event = fake_v11_group_message_event(message=OneBotV11Message("/argot"), user_id="2740324073")

        ctx.receive_event(bot, event)
        ctx.should_call_send(event, OneBotV11Message("需回复一条消息"))
        ctx.should_finished()


async def test_normal_get_argot_without_reply(app: App):
    from nonebot_plugin_argot.matcher import argot_cmd

    async with app.test_matcher(argot_cmd) as ctx:
        adapter = get_adapter(OneBotV11Adapter)
        bot = ctx.create_bot(base=OneBotV11Bot, adapter=adapter)
        event = fake_v11_group_message_event(message=OneBotV11Message("/argot"))

        ctx.receive_event(bot, event)
        ctx.should_call_send(event, OneBotV11Message("指令 Argot 仅允许 SUPERUSER 使用"))
        ctx.should_finished()
