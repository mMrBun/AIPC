import flet as ft


class MessageCard(ft.Card):
    def __init__(self, **kwargs):
        super(MessageCard, self).__init__(**kwargs)
        self.border_radius = 10
        self.color = ft.colors.BLUE
        self.blur = ft.Blur(1, 1)
        self.content = ft.Container(
            content=ft.Row(
                [
                    ft.Text(
                        "Image title",
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
                        alignment=ft.alignment.Alignment(0,0)
                    )
                ]
            )
        )
