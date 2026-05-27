import httpx
from mcp.types import CallToolResult, TextContent

from astrbot.api import AstrBotConfig
from astrbot.api.event import AstrMessageEvent, filter
from astrbot.api.star import Context, Star, register


@register(
    "astrbot_plugin_remote_resources",
    "lihz",
    "提供函数工具和标准接口。让AI可以读取远程系统的文件内容",
    "1.0.1",
)
class MyPlugin(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.config = config

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""

    @filter.llm_tool()
    async def get_user_remote_file_list(self, event: AstrMessageEvent):
        """
        获取用户所有文件列表。当用户要求查看、读取或处理某个文件，但你不知道具体 file_id 时，必须首先调用此函数。该函数会返回文件 ID (file_id)、文件名 (file_name) 以及文件大小等元数据。

        Returns:
            文件列表
        """

        async with httpx.AsyncClient(timeout=30) as client:
            try:
                response = await client.post(
                    url=self.config.get("file_list_api", ""),
                    json={
                        "session_id": event.session_id,
                        "token": self.config.get("token", ""),
                    },
                    headers={
                        "Accept": "application/json, text/plain, */*",
                        "Accept-Encoding": "gzip, deflate",
                        "Cache-Control": "no-cache",
                        "Connection": "keep-alive",
                        "Pragma": "no-cache",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:150.0) Gecko/20100101 Firefox/150.0",
                    },
                )
                if response.status_code != 200:
                    return CallToolResult(
                        content=[
                            TextContent(
                                type="text",
                                text=f"Error: 读取文件列表失败，http code：{response.status_code}，content：{response.text}",
                            )
                        ]
                    )
                return CallToolResult(
                    content=[TextContent(type="text", text=response.text)]
                )
            except Exception as e:
                return CallToolResult(
                    content=[
                        TextContent(
                            type="text", text=f"Error: 读取远程文件列表失败，{e}"
                        )
                    ]
                )

    @filter.llm_tool()
    async def get_user_remote_read_file(self, event: AstrMessageEvent, file_id: str):
        """
        根据指定的 file_id 读取并返回该文件的完整文本内容。
        注意： 严禁猜测 file_id。在调用此函数之前，你必须已经通过 read_list 获取了确切的 ID。如果用户提到的文件名不在最近一次 read_list 的结果中，请重新调用 read_list 确认。

        Args:
            file_id (string): 文件id

        Returns:
            文件内容
        """
        async with httpx.AsyncClient(timeout=30) as client:
            try:
                response = await client.post(
                    url=self.config.get("file_content_api", ""),
                    json={
                        "session_id": event.session_id,
                        "file_id": file_id,
                        "token": self.config.get("token", ""),
                    },
                    headers={
                        "Accept": "application/json, text/plain, */*",
                        "Accept-Encoding": "gzip, deflate",
                        "Cache-Control": "no-cache",
                        "Connection": "keep-alive",
                        "Pragma": "no-cache",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:150.0) Gecko/20100101 Firefox/150.0",
                    },
                )
                if response.status_code != 200:
                    return CallToolResult(
                        content=[
                            TextContent(
                                type="text",
                                text=f"Error: 读取文件列表失败，http code：{response.status_code}，content：{response.text}",
                            )
                        ]
                    )
                return CallToolResult(
                    content=[TextContent(type="text", text=response.text)]
                )
            except Exception as e:
                return CallToolResult(
                    content=[TextContent(type="text", text=f"Error: 读取文件内容失败，{e}")]
                )
