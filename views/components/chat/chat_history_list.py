import flet as ft
from apis.db import get_all_chats, new_chat, delete_chat

class MessageCard(ft.UserControl):
    def __init__(self, _id: int, title: str, on_select, on_delete=None, **kwargs):
        super().__init__(**kwargs)
        self.id = _id
        self.title = title
        self.on_select = on_select
        self.on_delete = on_delete
        self.build_ui()

    def build_ui(self):
        self.button = ft.OutlinedButton(
            content=ft.Row(
                controls=[
                    ft.Text(self.title),
                    ft.IconButton(icon=ft.icons.CLOSE, icon_size=10, on_click=self.delete_chat)
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )
        )
        self.button.on_click = self.select_chat

    def select_chat(self, e):
        if self.on_select:
            self.on_select(self.id)

    def delete_chat(self, e):
        delete_chat(self.id)
        if self.on_delete:
            self.on_delete()  # 调用回调以更新聊天列表

    def build(self):
        return self.button

class ChatHistoryList(ft.UserControl):
    def __init__(self, on_chat_selected, on_new_chat, **kwargs):
        super().__init__(**kwargs)
        self.on_chat_selected = on_chat_selected
        self.on_new_chat = on_new_chat
        self.build_ui()

    def build_ui(self):
        self.new_chat_button = ft.FilledButton(
            text="New Chat",
            icon=ft.icons.ADD,
            width=150,
            on_click=self.on_new_chat
        )

        self.chat_list = ft.Column(
            controls=[
                MessageCard(
                    _id=chat.id,
                    title=chat.title,
                    on_select=self.on_chat_selected,
                    on_delete=self.update_chat_list  # 传递回调
                )
                for chat in get_all_chats()
            ],
            spacing=5,
            scroll=ft.ScrollMode.AUTO
        )

        self.controls = [
            ft.Row(
                controls=[
                    self.new_chat_button
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            ft.Container(
                content=self.chat_list,
                expand=True
            )
        ]

    def update_chat_list(self):
        self.chat_list.controls = [
            MessageCard(
                _id=chat.id,
                title=chat.title,
                on_select=self.on_chat_selected,
                on_delete=self.update_chat_list  # 确保新消息卡片也传递回调
            )
            for chat in get_all_chats()
        ]
        self.update()

    def build(self):
        return ft.Column(
            controls=self.controls,
            expand=True
        )
