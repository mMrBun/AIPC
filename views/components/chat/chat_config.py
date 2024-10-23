import flet as ft

class ChatConfig(ft.UserControl):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.initialize_controls()

    def initialize_controls(self):
        self.controls = [
            ft.Text("聊天配置", size=20),
            # 可以在这里添加更多配置项
        ]

    def build(self):
        return ft.Column(
            controls=self.controls,
            alignment=ft.MainAxisAlignment.START,
            spacing=10
        )
