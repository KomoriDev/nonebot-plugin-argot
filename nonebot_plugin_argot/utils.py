from datetime import datetime, timedelta


def calculate_expired_at(expire_time: timedelta | int) -> datetime:
    """计算过期时间点"""
    create_at = datetime.now()
    if isinstance(expire_time, int):
        expire_time = timedelta(seconds=expire_time)

    expired_at = create_at + expire_time
    return expired_at
