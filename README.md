<!-- markdownlint-disable MD033 MD036 MD041 MD045 -->
<div align="center">
  <a href="https://v2.nonebot.dev/store">
    <img src="./docs/NoneBotPlugin.svg" width="300" alt="logo" />
  </a>

</div>

<div align="center">

# NoneBot-Plugin-Argot

_✨ NoneBot2 暗语消息 ✨_

<a href="">
  <img src="https://img.shields.io/pypi/v/nonebot-plugin-argot.svg" alt="pypi" />
</a>
<img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="python">
<a href="https://github.com/astral-sh/uv">
  <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json" alt="uv-managed">
</a>
<a href="https://github.com/nonebot/plugin-alconna">
  <img src="https://img.shields.io/badge/Alconna-resolved-2564C2" alt="alc-resolved">
</a>

<br/>

<a href="https://registry.nonebot.dev/plugin/nonebot-plugin-argot:nonebot_plugin_argot">
  <img src="https://img.shields.io/endpoint?url=https%3A%2F%2Fnbbdg.lgc2333.top%2Fplugin%2Fnonebot-plugin-argot" alt="NoneBot Registry" />
</a>
<a href="https://registry.nonebot.dev/plugin/nonebot-plugin-argot:nonebot_plugin_argot">
  <img src="https://img.shields.io/endpoint?url=https%3A%2F%2Fnbbdg.lgc2333.top%2Fplugin-adapters%2Fnonebot-plugin-argot" alt="Supported Adapters" />
</a>

<br />
<a href="#-效果图">
  <strong>📸 演示与预览</strong>
</a>
&nbsp;&nbsp;|&nbsp;&nbsp;
<a href="#-安装">
  <strong>📦️ 下载插件</strong>
</a>
&nbsp;&nbsp;|&nbsp;&nbsp;
<a href="https://qm.qq.com/q/Vuipof2zug" target="__blank">
  <strong>💬 加入交流群</strong>
</a>

</div>

## 📖 介绍

NoneBot2 暗语消息支持

> [!IMPORTANT]
> **收藏项目**，你将从 GitHub 上无延迟地接收所有发布通知～⭐️

<img width="100%" src="https://starify.komoridevs.icu/api/starify?owner=KomoriDev&repo=nonebot-plugin-argot" alt="starify" />

<details>
  <summary><kbd>Star History</kbd></summary>
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=KomoriDev/nonebot-plugin-argot&theme=dark&type=Date" />
    <img width="100%" src="https://star-history.com/#KomoriDev/nonebot-plugin-argot&Date" />
  </picture>
</details>

## 💿 安装

以下提到的方法任选 **其一** 即可

<details open>
<summary>[推荐] 使用 nb-cli 安装</summary>
在 Bot 的根目录下打开命令行, 输入以下指令即可安装

```bash
nb plugin install nonebot-plugin-argot
```

</details>
<details>
<summary>使用包管理器安装</summary>

```bash
pip install nonebot-plugin-argot
# or, use poetry
poetry add nonebot-plugin-argot
# or, use pdm
pdm add nonebot-plugin-argot
# or, use uv
uv add nonebot-plugin-argot
```

</details>

## 🎉 使用

本插件基于 [plugin-alconna](https://github.com/nonebot/plugin-alconna)，为 NoneBot 提供了一个新的消息段 `Argot`

```py
@dataclass
class Argot(Segment):
    name: str
    segment: str | Segment | list[Segment]
    command: str | Literal[False] | None = field(default=None, kw_only=True)
    expired_at: int | timedelta = field(default_factory=timedelta, kw_only=True)
    extra: dict[str, Any] = field(default_factory=dict, kw_only=True)
```

- `name`: 暗语名称
- `segment`: 暗语包含的消息段
- `command`: 触发暗语的指令（跟随 `COMMAND_START` 配置）
  - `None`: 使用 `name` 作为指令名
  - `False`: 禁止通过指令获取暗语
- `expired_at`: 过期时间
- `extra`：暗语事件中储存的额外数据

可以通过 `on_argot` 监听暗语事件

```py
@on_argot("name")
async def _(event: ArgotEvent):
  ...
```

示例：👉 [传送门](./example/plugins/demo.py)

## 📸 效果图

<img src="./docs/example_1.png" height="400" alt="example"/> <img src="./docs/example_2.png" height="400" alt="example"/>

## 💖 鸣谢

- [`KiramiBot`](https://github.com/A-kirami/KiramiBot)：灵感来源
- [`KomoriDev/Starify`](https://github.com/KomoriDev/Starify)：提供了引人注目的徽章
- [`ArcletProject/Letoderea`](https://github.com/ArcletProject/Letoderea)：高性能，结构简洁的事件系统

### 贡献者们

<a href="#-鸣谢">
  <img src="https://img.shields.io/badge/all_contributors-3-orange.svg?style=flat-square" alt="contributors" />
</a>
<a href="https://afdian.com/@komoridev">
  <img src="https://img.shields.io/badge/all_sponsors-17-946ce6.svg?style=flat-square" alt="sponsors" />
</a>

感谢这些大佬对本项目作出的贡献:

<a href="https://github.com/KomoriDev/nonebot-plugin-argot/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=KomoriDev/nonebot-plugin-argot&max=1000" alt="contributors" />
</a>

## 📄 许可证

本项目使用 MIT 许可证开源

```txt
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

```
