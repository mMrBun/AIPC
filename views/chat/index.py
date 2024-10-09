import flet as ft

name = "Chat Page"
description = "Chat Page"


def build_page():
    main_structure = ft.Container(
        bgcolor=ft.colors.BLUE,
        content=ft.Row(
            spacing=0,
            controls=[
                ft.Container(
                    ft.Column(
                        controls=[
                            ft.Text("Chat"),
                        ],
                    ),
                    border=ft.Border(
                        top=ft.BorderSide(color=ft.colors.RED, width=2),
                        right=ft.BorderSide(color=ft.colors.RED, width=2),
                        bottom=ft.BorderSide(color=ft.colors.RED, width=2),
                        left=ft.BorderSide(color=ft.colors.RED, width=2),
                    ),
                    width=200,
                ),
                ft.Container(
                    ft.Column(
                        controls=[
                            ft.Text("Chat"),
                        ],

                    ),
                    border=ft.Border(
                        top=ft.BorderSide(color=ft.colors.BLACK, width=2),
                        right=ft.BorderSide(color=ft.colors.BLACK, width=2),
                        bottom=ft.BorderSide(color=ft.colors.BLACK, width=2),
                        left=ft.BorderSide(color=ft.colors.BLACK, width=2),
                    ),
                    expand=1,
                ),
                ft.Container(
                    ft.Column(
                        controls=[
                            ft.Text("Chat"),
                        ],
                    ),
                    border=ft.Border(
                        top=ft.BorderSide(color=ft.colors.PINK, width=2),
                        right=ft.BorderSide(color=ft.colors.PINK, width=2),
                        bottom=ft.BorderSide(color=ft.colors.PINK, width=2),
                        left=ft.BorderSide(color=ft.colors.PINK, width=2),
                    ),
                    width=200,
                ),
            ]
        ),
    )

    return main_structure
