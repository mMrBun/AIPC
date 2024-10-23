import flet as ft

class EmptyChatPage(ft.UserControl):
    def build(self):
        # 顶部标题
        title = ft.Text(
            "有什么可以帮忙的?",
            size=32,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER,
            font_family="OPPOSans",

        )

        # 按钮
        buttons = [
            ft.ElevatedButton(text="制定计划", icon=ft.icons.LIGHTBULB_OUTLINE,
                              color=ft.colors.YELLOW),
            ft.ElevatedButton(text="总结文本", icon=ft.icons.DESCRIPTION,
                              color=ft.colors.ORANGE),
            ft.ElevatedButton(text="帮我写", icon=ft.icons.EDIT,  color=ft.colors.PURPLE),
            ft.ElevatedButton(text="更多", icon=ft.icons.MORE_HORIZ,  color=ft.colors.GREY),
        ]

        # 按钮容器
        button_container = ft.Row(
            buttons,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10
        )


        return ft.Column(
            [
                ft.Placeholder(color=ft.colors.TRANSPARENT, fallback_height=100),
                title,
                button_container,
                ft.Placeholder(color=ft.colors.TRANSPARENT, fallback_height=100),
            ],

            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=50,
        )