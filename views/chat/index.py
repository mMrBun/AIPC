import uuid

import flet as ft
from views.components.chat.chat_dialog import ChatDialog
from views.components.chat.chat_history_list import ChatHistoryList
from views.components.chat.chat_config import ChatConfig
from apis.db import new_chat

class MainPage(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.chat_history_list = ChatHistoryList(on_new_chat=self.create_before_chat, on_chat_selected=self.on_chat_selected)
        self.chat_dialog = ChatDialog(on_chat_updated=self.refresh_chat_dialog, on_new_chat=self.create_after_chat)
        self.chat_config = ChatConfig()


    def create_before_chat(self, e):
        new_chat_id = new_chat(title=uuid.uuid4().hex)
        self.chat_history_list.update_chat_list()
        self.chat_dialog.load_chat(new_chat_id)

    def create_after_chat(self):
        new_chat_id = new_chat(title=uuid.uuid4().hex)
        self.chat_dialog.current_chat_id = new_chat_id
        self.chat_history_list.update_chat_list()

    def on_chat_selected(self, chat_id):
        self.chat_dialog.load_chat(chat_id)
        self.chat_dialog.update()

    def refresh_chat_dialog(self, chat_id):
        self.chat_dialog.load_chat(chat_id)

    def build(self):
        main_structure = ft.Row(
            controls=[
                ft.Container(
                    content=self.chat_history_list,
                    width=150,
                    margin=ft.margin.only(left=10)
                ),
                ft.VerticalDivider(width=1),
                ft.Container(
                    content=self.chat_dialog,
                    expand=True
                ),
                ft.VerticalDivider(width=1),
                ft.Container(
                    content=self.chat_config,
                    width=200
                )
            ],
            expand=True
        )
        return main_structure
