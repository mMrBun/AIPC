import flet as ft
from views.components.chat.chat_dialog import ChatDialog
from views.components.chat.message_card import MessageCard

def build_page():

    main_structure = ft.Row(
        controls=[
            ft.Container(
                content=MessageCard.build_all_chat(),
                width=150,
                margin=ft.margin.only(left=10)
            ),
            ft.VerticalDivider(width=1, trailing_indent=1),
            ft.Container(
                content=ChatDialog(),
                expand=1
            )
        ],
        expand=True
    )

    return main_structure

# ft.Container(
#     content=ft.Column(
#         controls=[
#             ft.Text(value="Config 1"),
#             ft.Text(value="Config 2"),
#             ft.Text(value="Config 3"),
#             # Add more config items here
#         ]
#     ),
#     width=200  # Fixed width for the config column
# )
