import nonebot

from nonebot.adapters.onebot.v11 import Adapter as ONEBOT_V11Adapter


nonebot.init()

driver = nonebot.get_driver()
driver.register_adapter(ONEBOT_V11Adapter)

nonebot.load_plugin("nonebot_plugin_argot")

if __name__ == "__main__":
    nonebot.run()
