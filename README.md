# astrbot_plugin_remote_resources
本工具可以让AI自动读取来将外部项目的资料
提供两个函数工具

## get_user_remote_file_list
获取文件列表，以JSON POST请求外部项目，
请求参数：

| 参数 | 类型 |
|----|----|
| session_id | string |
| token | string |

外部项目需要返回json文本数据，格式如下：
```json
[
  {
    "file_id": "文件编号( 必须)",
    "file_name": "文件名 (必须)",
    "desc": "文件介绍 (可选)",
    "size": "文件大小 (可选)"
  }
]
```

## get_user_remote_read_file
读取文件内容，以JSON POST请求外部项目，请求参数：

| 参数 | 类型 |
|----|----|
| file_id | string |
| session_id | string |
| token | string |

外部项目直接返回文件内容
