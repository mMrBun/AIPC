import flet as ft


class MessageCard(ft.OutlinedButton):
    def __init__(self, _id: int, title: str, update_callback, **kwargs):
        super(MessageCard, self).__init__(**kwargs)
        self.title = title
        self.id = _id
        self.update_callback = update_callback
        # self.width = 100
        self.content = ft.Row(
            controls=[
                ft.Text(self.title),
                ft.IconButton(icon=ft.icons.CLOSE, icon_size=10, on_click=self.delete_chat)],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN)


    def delete_chat(self, e):
        from apis.db import delete_chat
        delete_chat(_id=self.id)
        self.update_callback()


    @staticmethod
    def build_all_chat():
        from apis.db import get_all_chats, new_chat

        def add_new_chat(e):
            new_chat(title="New Chat")
            update_chat_list(left_chat_message)

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
                        controls=[MessageCard(_id=chat.id, title=str(chat.title),
                                              update_callback=lambda: update_chat_list(left_chat_message)) for chat in
                                  chat_list],
                        scroll=ft.ScrollMode.ALWAYS
                    ),
                    expand=True  # This makes the container take all available space
                )
            ],
        )
        return left_chat_message


def update_chat_list(left_chat_message):
    from apis.db import get_all_chats
    chat_list = get_all_chats()
    left_chat_message.controls[1].content.controls = [MessageCard(_id=chat.id, title=str(chat.title), update_callback=lambda: update_chat_list(left_chat_message)) for chat in chat_list]
    left_chat_message.update()

