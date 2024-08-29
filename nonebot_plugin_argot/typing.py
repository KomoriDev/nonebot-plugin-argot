from datetime import timedelta
from typing_extensions import TypedDict, NotRequired


class ArgotArgs(TypedDict):
    """暗语参数"""

    name: str
    """暗语名称"""
    content: str
    """暗语内容"""
    message_id: str
    """存放暗语的消息 ID"""
    command: NotRequired[str]
    """用户触发指令（输入该指令查看暗语）"""
    expired_time: NotRequired[timedelta | int]
    """过期时间"""
