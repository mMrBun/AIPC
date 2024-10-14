import flet as ft
from views.components.chat.chat_dialog import ChatDialog
name = "Chat Page"
description = "Chat Page"


def build_page():
    main_structure = ft.Row(
        controls=[
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(value="History 1"),
                        ft.Text(value="History 2"),
                        ft.Text(value="History 3"),
                        # Add more history items here
                    ]
                ),
                width=200  # Fixed width for the history column
            ),
            ft.Container(
                content=ChatDialog(),
                expand=1  # This makes the chat column take up the remaining space
            ),
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(value="Config 1"),
                        ft.Text(value="Config 2"),
                        ft.Text(value="Config 3"),
                        # Add more config items here
                    ]
                ),
                width=200  # Fixed width for the config column
            )
        ],
        expand=True
    )

    return main_structure
