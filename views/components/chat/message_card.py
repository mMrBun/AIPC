import flet as ft


class MessageCard(ft.Card):
    def __init__(self, **kwargs):
        super(MessageCard, self).__init__(**kwargs)
        self.content = ft.Container(
                content=ft.Column(
                    [
                        ft.Row(
                            alignment=ft.MainAxisAlignment.END,
                            controls=[ft.IconButton(icon=ft.icons.CLOSE, icon_size=10)],
                            height=20
                        ),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[ft.Text("打招呼", text_align=ft.TextAlign.CENTER)]
                        )
                    ],
                    spacing=0
                ),
                width=150,
                height=60
            )
