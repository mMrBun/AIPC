# chat_dialog.py
import json
from typing import List

import flet as ft

from apis.db import get_chat_messages_by_chat_id
from apis.protocol import ChatMessage, Role, MultimodalInputItem
from apis.llms.llm_xpu import generate

class ChatDialog(ft.Column):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.messages = []
        self.list_view = ft.ListView(
            controls=[],
            expand=True,
            auto_scroll=True,
            padding=0,
        )
        self.input_control = ft.TextField(
            value="",
            multiline=True,
            min_lines=1,
            border_radius=15,
            border=ft.InputBorder.OUTLINE,
            content_padding=ft.Padding(10, 10, 10, 10),
            on_submit=self.send_message,
            label="Enter to send message,Shift+Enter to new line",
            filled=True,
            shift_enter=True,
            suffix_icon=ft.icons.SEND_ROUNDED
        )

        self.controls = [
            ft.Container(
                content=self.list_view,
                expand=True,
                padding=10,
            ),
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.IconButton(
                            icon=ft.icons.ATTACH_FILE,
                            tooltip="Attach file",
                            rotate=35
                        ),
                        ft.Container(
                            content=self.input_control,
                            expand=True
                        )
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                ),
                padding=ft.padding.all(10)
            )
        ]

    def load_chat(self, chat_id):
        """加载指定聊天 ID 的消息"""
        self.messages = get_chat_messages_by_chat_id(chat_id)
        if self.messages:
            self.list_view.controls = self.build_message(self.messages)
        else:
            self.list_view.controls = []
        self.update()

    def build_message_control(self, content, role):
        # 现有的构建消息的方法
        if role == 'user':
            avatar = ft.Icon(ft.icons.PERSON, size=40)
        else:
            avatar = ft.Icon(ft.icons.AIR, size=40)

        # 移除 expand=True 以允许文本换行
        bubble_content = ft.Markdown(
            value=content,
            selectable=True,
            extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
            code_theme=ft.MarkdownCodeTheme.ATOM_ONE_DARK,
            code_style=ft.TextStyle(font_family="Roboto Mono"),
            on_tap_link=lambda e: self.page.launch_url(e.data),
            # expand=True  # 移除此行
        )

        # 添加 max_width 以限制气泡的最大宽度，避免过宽
        bubble = ft.Container(
            content=bubble_content,
            padding=ft.Padding(10,10,10,10),
            margin=ft.Margin(0, 0, 0, 10),
            border=ft.Border(
                left=ft.BorderSide(width=1),
                right=ft.BorderSide(width=1),
                top=ft.BorderSide(width=1),
                bottom=ft.BorderSide(width=1)
            ),
            border_radius=ft.border_radius.all(10),
            # 设置最大宽度，例如 500 像素，可根据需要调整
            # max_width=500,
            # 确保容器内部内容可以换行
            # expand=True
        )

        if role == 'user':
            message_row = ft.Row(
                [
                    ft.Container(
                        content=bubble,
                        margin=ft.margin.symmetric(horizontal=10),
                        expand=True  # 确保气泡可以根据需要扩展，但不超过 max_width
                    ),
                    avatar,
                ],
                alignment=ft.MainAxisAlignment.END,
                vertical_alignment=ft.CrossAxisAlignment.START,
                # expand=True
            )
        else:
            message_row = ft.Row(
                [
                    avatar,
                    ft.Container(
                        content=bubble,
                        margin=ft.margin.symmetric(horizontal=10),
                        expand=True  # 确保气泡可以根据需要扩展，但不超过 max_width
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.START,
                # expand=True

            )
        return message_row

    def build_message(self, msg):
        content = msg.history_content
        messages = convert_history_to_chat_messages(content)
        controls = []
        for message in messages:
            message_row = self.build_message_control(message.content, message.role)
            controls.append(message_row)
        return controls

    def send_message(self, e):
        # 你需要实现发送消息的逻辑
        message = e.control.value
        message_row = self.build_message_control(message, 'user')
        self.list_view.controls.append(message_row)
        self.input_control.value = ""
        self.input_control.disabled = True
        generator = generate(message)
        assistant_row = self.build_message_control("", 'system')
        self.list_view.controls.append(assistant_row)
        self.update()
        content = ""
        for chunk in generator:
            content += chunk
            assistant_row.controls[1].content.content.value = content
            assistant_row.update()
        self.input_control.disabled = False
        self.update()



def convert_history_to_chat_messages(history_str: str) -> List[ChatMessage]:
    """
    将历史消息的JSON字符串转换为ChatMessage对象列表。

    :param history_str: 历史消息的JSON字符串
    :return: ChatMessage对象的列表
    """
    try:
        # 解析JSON字符串
        history_data = json.loads(history_str)

        chat_messages = []
        for msg in history_data:
            # 获取角色并转换为Role枚举
            role_str = msg.get("role")
            if role_str not in Role.__members__.values():
                raise ValueError(f"未知的角色: {role_str}")
            role = Role(role_str)

            # 获取内容，可以是字符串或多模态输入项的列表
            content = msg.get("content")
            if isinstance(content, str):
                content_parsed = content
            elif isinstance(content, list):
                content_parsed = [MultimodalInputItem(**item) for item in content]
            else:
                content_parsed = None  # 或者根据需求处理其他类型

            # 创建ChatMessage实例
            chat_message = ChatMessage(
                role=role,
                content=content_parsed
                # 如果有tool_calls，可以在这里处理并赋值
            )

            chat_messages.append(chat_message)

        return chat_messages

    except json.JSONDecodeError as e:
        print("JSON解析错误:", e)
        return []
    except Exception as e:
        print("转换过程中发生错误:", e)
        return []
