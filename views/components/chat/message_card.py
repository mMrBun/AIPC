# message_card.py

import flet as ft

class MessageCard(ft.OutlinedButton):
    def __init__(self, _id: int, title: str, update_callback, on_chat_selected, **kwargs):
        super(MessageCard, self).__init__(**kwargs)
        self.title = title
        self.id = _id
        self.update_callback = update_callback
        self.on_chat_selected = on_chat_selected

        self.content = ft.Row(
            controls=[
                ft.Text(self.title),
                ft.IconButton(icon=ft.icons.CLOSE, icon_size=10, on_click=self.delete_chat)
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )
        self.on_click = self.select_chat

    def select_chat(self, e):
        self.on_chat_selected(self.id)

    def delete_chat(self, e):
        from apis.db import delete_chat
        delete_chat(_id=self.id)
        self.update_callback()

    @staticmethod
    def update_chat_list(left_chat_message, on_chat_selected):
        from apis.db import get_all_chats
        chat_list = get_all_chats()
        left_chat_message.controls[1].content.controls = [
            MessageCard(
                _id=chat.id,
                title=str(chat.title),
                update_callback=lambda: MessageCard.update_chat_list(left_chat_message, on_chat_selected),
                on_chat_selected=on_chat_selected
            ) for chat in chat_list
        ]
        left_chat_message.update()

    @staticmethod
    def build_all_chat(on_chat_selected):
        from apis.db import get_all_chats, new_chat

        def add_new_chat(e):
            new_chat(title="New Chat")
            MessageCard.update_chat_list(left_chat_message, on_chat_selected)

        chat_list = get_all_chats()
        left_chat_message = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.FilledButton("New Chat", icon=ft.icons.ADD, width=150, on_click=add_new_chat),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            MessageCard(
                                _id=chat.id,
                                title=str(chat.title),
                                update_callback=lambda: MessageCard.update_chat_list(left_chat_message, on_chat_selected),
                                on_chat_selected=on_chat_selected  # 正确传递回调
                            ) for chat in chat_list
                        ],
                        scroll=ft.ScrollMode.ALWAYS
                    ),
                    expand=True
                )
            ],
        )
        return left_chat_message


