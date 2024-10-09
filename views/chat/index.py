import flet as ft
from views.components.chat.message_card import MessageCard
name = "Chat Page"
description = "Chat Page"


def build_page():
    chat_history = ft.ListView(expand=1, spacing=10, padding=20)
    for i in range(10):
        chat_history.controls.append(
            MessageCard()
        )
    main_structure = ft.Container(
        content=ft.Row(
            spacing=0,
            controls=[
                ft.Container(
                    ft.Column(
                        controls=[
                            chat_history
                        ],
                    ),
                    width=180,
                ),
                ft.Container(
                    ft.Column(
                        controls=[
                            ft.Text("Chat"),
                        ],

                    ),
                    expand=1,
                ),
                ft.Container(
                    ft.Column(
                        controls=[
                            ft.Text("Chat"),
                        ],
                    ),
                    width=100,
                ),
            ]
        ),
    )

    return main_structure
