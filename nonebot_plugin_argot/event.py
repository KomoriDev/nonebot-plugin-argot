from collections.abc import Callable
from typing import Any, TypeVar, ParamSpec

import arclet.letoderea as le
from nonebot.adapters import Bot
from nonebot_plugin_alconna.uniseg import Target

from .typing import Argot

T = TypeVar("T")
P = ParamSpec("P")


@le.make_event
class ArgotEvent:
    name: str
    data: Argot
    target: Target
    extra: dict[str, Any]

    async def get_bot(self) -> Bot:
        return await self.target.select()


def on_argot(name: str):
    def wrapper(func: Callable[P, T]):
        subscriber = le.on(ArgotEvent, func)
        subscriber = le.enter_if(le.deref(ArgotEvent).name == name)(subscriber)
        return subscriber

    return wrapper
