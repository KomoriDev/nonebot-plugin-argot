from pathlib import Path

import pytest
import nonebot
from sqlalchemy import StaticPool, delete
from nonebug import NONEBOT_INIT_KWARGS, App
from nonebot.adapters.onebot.v11 import Adapter as OneBotV11Adapter


def pytest_configure(config: pytest.Config):
    config.stash[NONEBOT_INIT_KWARGS] = {
        "driver": "~fastapi",
        "log_level": "DEBUG",
        "command_start": {"/", ""},
        "superusers": {"2740324073"},
        "sqlalchemy_database_url": "sqlite+aiosqlite://",
        "sqlalchemy_engine_options": {"poolclass": StaticPool},
        "alembic_startup_check": False,
        "argot__url_to_image": False,
    }


@pytest.fixture
async def app(tmp_path: Path):
    # 加载插件
    nonebot.require("nonebot_plugin_argot")

    from nonebot_plugin_orm import init_orm, get_session

    await init_orm()
    yield App()

    from nonebot_plugin_argot.model import Argot

    async with get_session() as session, session.begin():
        await session.execute(delete(Argot))


@pytest.fixture(scope="session", autouse=True)
def _load_adapters(nonebug_init: None):
    driver = nonebot.get_driver()
    driver.register_adapter(OneBotV11Adapter)
