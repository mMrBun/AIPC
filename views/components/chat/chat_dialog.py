import flet as ft

class ChatDialog(ft.Column):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.controls = [
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(value="asd")
                    ],
                    scroll=ft.ScrollMode.AUTO
                ),
                expand=True,
                # height=50  # 70% of the height
            ),
            ft.Container(
                content=ft.TextField(value="zxc"),
                # height=50  # 30% of the height
            )
        ]