# chat_dialog.py
import json
from typing import List

import flet as ft
from views.components.chat.empty_chat_page import EmptyChatPage
from apis.db import get_chat_messages_by_chat_id, update_chat_message, new_chat
from apis.protocol import ChatMessage, Role, MultimodalInputItem
from apis.llms.llm_xpu import generate

class ChatDialog(ft.UserControl):
    def __init__(self, on_chat_updated=None, on_new_chat=None, **kwargs):
        super().__init__(**kwargs)
        self.messages = []
        self.current_chat_id = None
        self.on_chat_updated = on_chat_updated
        self.on_new_chat = on_new_chat
        self.load = False
        # 初始化UI组件
        self.list_view = ft.ListView(
            expand=True,
            auto_scroll=True,
            padding=0,
            controls=[
                EmptyChatPage()
            ]
        )
        self.input_control = ft.TextField(
            value="",
            multiline=True,
            min_lines=1,
            border_radius=15,
            border=ft.InputBorder.OUTLINE,
            content_padding=ft.Padding(10, 10, 10, 10),
            on_submit=self.send_message,
            label="Enter to send message, Shift+Enter to new line",
            filled=True,
            shift_enter=True,
            suffix_icon=ft.icons.SEND_ROUNDED,
            text_style=ft.TextStyle(overflow=ft.TextOverflow.FADE)
        )

        self.build_ui()

    def build_ui(self):
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

    def build_message_control(self, content, role):
        if role == Role.USER:
            avatar = ft.Icon(ft.icons.PERSON, size=40)
        else:
            avatar = ft.Icon(ft.icons.AIR, size=40)

        bubble_content = ft.Markdown(
            value=content,
            selectable=True,
            extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
            code_theme=ft.MarkdownCodeTheme.ATOM_ONE_DARK,
            code_style=ft.TextStyle(font_family="Roboto Mono", overflow=ft.TextOverflow.FADE),
            on_tap_link=lambda e: self.page.launch_url(e.data),
        )

        bubble = ft.Container(
            content=bubble_content,
            padding=ft.Padding(10, 10, 10, 10),
            margin=ft.Margin(0, 0, 0, 10),
            border=ft.border.all(width=1),
            border_radius=ft.border_radius.all(10),
        )

        if role == Role.USER:
            message_row = ft.Row(
                [
                    ft.Container(
                        content=bubble,
                        margin=ft.margin.symmetric(horizontal=10),
                    ),
                    avatar,
                ],
                wrap=True,
                alignment=ft.MainAxisAlignment.END,
            )
        else:
            message_row = ft.Row(
                [
                    avatar,
                    ft.Container(
                        content=bubble,
                        margin=ft.margin.symmetric(horizontal=10),
                    ),
                ],
                wrap=True,
                alignment=ft.MainAxisAlignment.START,
            )
        return message_row

    def build_message(self, msg):
        content = msg.history_content
        chat_history = json.loads(content)
        self.messages = chat_history
        messages = convert_history_to_chat_messages(content)
        controls = [self.build_message_control(message.content, message.role) for message in messages]
        return controls

    def load_chat(self, chat_id):
        """加载指定聊天 ID 的消息"""
        self.current_chat_id = chat_id
        chat_history = get_chat_messages_by_chat_id(chat_id)
        if chat_history:
            self.load = True
            self.list_view.controls = self.build_message(chat_history)
            self.input_control.disabled = False
        else:
            self.load = False
            self.list_view.controls = []
            empty_chat_page = EmptyChatPage()
            self.list_view.controls.append(empty_chat_page)
            self.input_control.disabled = False
        self.update()

    def send_message_async(self, message: str):

        user_message = {"role": Role.USER, "content": message}
        self.messages.append(user_message)
        self.list_view.controls.append(self.build_message_control(message, Role.USER))
        self.update()


        assistant_row = self.build_message_control("", Role.ASSISTANT)
        self.list_view.controls.append(assistant_row)
        self.update()


        content = ""
        for chunk in generate(message):
            content += chunk
            assistant_row.controls[1].content.content.value = content
            assistant_row.update()

        assistant_message = {"role": Role.ASSISTANT, "content": content}
        self.messages.append(assistant_message)
        content_json = json.dumps(self.messages, ensure_ascii=False)
        update_chat_message(self.current_chat_id, content_json)

        self.input_control.disabled = False
        self.input_control.value = ""
        self.update()

    def send_message(self, e):
        if not self.load:
            self.list_view.controls = []
            self.on_new_chat()
            self.load = True
        message = e.control.value.strip()
        if message:
            self.input_control.disabled = True
            self.send_message_async(message)

    def build(self):
        return ft.Column(
            controls=self.controls,
            expand=True
        )

def convert_history_to_chat_messages(history_str: str) -> List[ChatMessage]:
    try:
        history_data = json.loads(history_str)

        chat_messages = []
        for msg in history_data:
            role_str = msg.get("role")
            if role_str not in Role._value2member_map_:
                raise ValueError(f"未知的角色: {role_str}")
            role = Role(role_str)

            content = msg.get("content")
            if isinstance(content, str):
                content_parsed = content
            elif isinstance(content, list):
                content_parsed = [MultimodalInputItem(**item) for item in content]
            else:
                content_parsed = None

            chat_message = ChatMessage(
                role=role,
                content=content_parsed
            )
            chat_messages.append(chat_message)

        return chat_messages

    except json.JSONDecodeError as e:
        print("JSON parse error:", e)
        return []
    except Exception as e:
        print("parse error during transfer", e)
        return []
