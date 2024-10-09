import flet as ft

def main(page: ft.Page):
    page.title = "Flet Expand Example"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # 创建一个 Container 并设置 expand=True
    container = ft.Container(
        content=ft.Text("This container fills all available space"),
        bgcolor=ft.colors.BLUE,
        expand=True
    )

    # 将 Container 添加到页面
    page.add(container)

# 运行应用
ft.app(target=main)
