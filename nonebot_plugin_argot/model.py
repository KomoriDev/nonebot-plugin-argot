from functools import wraps
from collections.abc import Sequence
from datetime import datetime, timedelta

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Text, String, and_, delete, select
from nonebot_plugin_orm import Model, get_session, get_scoped_session

from .utils import calculate_expired_at


class Argot(Model):
    message_id: Mapped[str] = mapped_column(primary_key=True)
    """Message ID"""
    name: Mapped[str] = mapped_column(String(20), primary_key=True)
    """Argot Name"""
    content: Mapped[str] = mapped_column(Text)
    """Argot Content"""
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    """Create Time"""
    expired_at: Mapped[datetime] = mapped_column(nullable=True)
    """Expire time"""


async def add_argot(
    name: str,
    message_id: str,
    *,
    content: str | int,
    command: str | None = None,
    expire_time: timedelta | int | None = None,
) -> None:
    from .matcher import argot_cmd

    if expire_time:
        expired_at = calculate_expired_at(expire_time)
    else:
        expired_at = None

    if command:
        argot_cmd.shortcut(command, {"command": f"argot {name}", "prefix": True, "fuzzy": False})

    session = get_session()
    async with session.begin():
        argot = Argot(name=name, message_id=message_id, content=content, expired_at=expired_at)
        session.add(argot)


async def delete_expired_argots() -> None:
    session = get_scoped_session()
    await session.execute(delete(Argot).where(Argot.expired_at < datetime.now()))
    await session.commit()


def clean_expired_data(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        await delete_expired_argots()
        return await func(*args, **kwargs)

    return wrapper


@clean_expired_data
async def get_argot(name: str, message_id: str) -> Argot | None:
    session = get_scoped_session()
    stmt = select(Argot).where(and_(Argot.name == name, Argot.message_id == message_id))
    argot = (await session.execute(stmt)).scalar()
    return argot


@clean_expired_data
async def get_argots(message_id: str) -> Sequence[Argot] | None:
    session = get_scoped_session()

    stmt = select(Argot).where(
        Argot.message_id == message_id, (Argot.expired_at.is_(None)) | (Argot.expired_at > datetime.now())
    )

    argots = (await session.execute(stmt)).scalars().all()

    if not argots:
        return None

    return argots
