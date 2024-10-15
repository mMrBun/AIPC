import flet as ft
from pygments.styles.dracula import background


def main(page: ft.Page):
    page.title = "Card Example"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.them = page.light_theme = ft.theme.Theme(
        color_scheme_seed=ft.colors.random_color()
    )
    def change_them(e):
        if page.theme_mode == ft.ThemeMode.LIGHT:
            page.theme_mode = ft.ThemeMode.DARK
            page.theme = page.dark_theme = ft.theme.Theme(
                color_scheme_seed=ft.colors.random_color()
            )
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
            page.theme = page.light_theme = ft.theme.Theme(
                color_scheme_seed=ft.colors.random_color()
            )
        page.update()
    page.add(
        ft.IconButton(
            icon=ft.icons.LIGHT_MODE,
            on_click=change_them,
        ),
        ft.OutlinedButton(content=ft.Row(controls=[ft.Text("New Chat"),ft.TextButton("X")], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)),
    )


ft.app(main)