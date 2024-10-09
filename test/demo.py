import flet as ft

def main(page):
    page.title = "卡片示例"
    page.add(
        ft.Card(
            content=ft.Container(
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
        )
    )

ft.app(target=main)
