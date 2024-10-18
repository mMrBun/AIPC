# index.py

import flet as ft
from views.components.chat.chat_dialog import ChatDialog
from views.components.chat.message_card import MessageCard

def build_page():
    chat_dialog = ChatDialog()

    def on_chat_selected(chat_id):
        chat_dialog.load_chat(chat_id)

    left_chat_message = MessageCard.build_all_chat(on_chat_selected)

    main_structure = ft.Row(
        controls=[
            ft.Container(
                content=left_chat_message,
                width=150,
                margin=ft.margin.only(left=10)
            ),
            ft.VerticalDivider(width=1, trailing_indent=1),
            ft.Container(
                content=chat_dialog,
                expand=True,

            ),
            ft.VerticalDivider(width=1, trailing_indent=1),
            ft.Container(
                content=ft.Text("zzz"),
                width=200
            )
        ],
        expand=True
    )

    return main_structure
