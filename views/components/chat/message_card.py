import flet as ft


class MessageCard(ft.Card):
    def __init__(self, _id: int, title: str, **kwargs):
        super(MessageCard, self).__init__(**kwargs)
        self.border_radius = 10
        self.color = ft.colors.BLUE
        self.blur = ft.Blur(1, 1)
        self.title = title
        self.id = _id
        self.content = ft.Container(
            content=ft.Row(
                [
                    ft.Text(
                        self.title,
                        size=20,
                        opacity=0.5,
                        color=ft.colors.WHITE,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.IconButton(
                        icon=ft.icons.CLOSE,
                        width=20,
                        height=20,
                        icon_size=10,
                        alignment=ft.alignment.Alignment(0, 0),
                        on_click=self.delete_chat
                    )
                ]
            )
        )


    def delete_chat(self, e):
        from apis.db import delete_chat
        delete_chat(_id=self.id)



    @staticmethod
    def view_all_chat():
        from apis.db import get_all_chats, new_chat

        def update_chat_list():
            chat_list = get_all_chats()
            left_chat_message.controls[1].controls = [MessageCard(_id=chat.id, title=str(chat.title)) for chat in chat_list]
            left_chat_message.update()

        def add_new_chat(e):
            new_chat(title="New Chat")
            update_chat_list()

        chat_list = get_all_chats()
        left_chat_message = ft.Column(
            controls=[
                ft.FilledButton("New Chat", icon=ft.icons.ADD, on_click=add_new_chat),
                ft.Column(
                    controls=[MessageCard(_id=chat.id, title=str(chat.title)) for chat in chat_list]
                )
            ]
        )
        return left_chat_message


