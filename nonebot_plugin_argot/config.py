from nonebot import get_plugin_config
from pydantic import Field, BaseModel


class ScopedConfig(BaseModel):
    url_to_image: bool = True
    """暗语中的 url 自动转为图片"""


class Config(BaseModel):
    argot: ScopedConfig = Field(default_factory=ScopedConfig)
    """Argot Plugin Config"""


plugin_config = get_plugin_config(Config).argot
