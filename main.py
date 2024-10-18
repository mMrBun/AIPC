import logging


import flet as ft

from views.components.gallery_view import GalleryView
from gallerydata import GalleryData
from alembic import command
from alembic.config import Config

gallery = GalleryData()

logging.basicConfig(level=logging.INFO)

def run_migrations():
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")

def main(page: ft.Page):
    page.title = "AIPC"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.on_error = lambda e: print("Page error:", e.data)
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.fonts = {
        "Roboto Mono": "RobotoMono-VariableFont_wght.ttf",
        "RobotoSlab": "RobotoSlab[wght].ttf",
    }
    page.theme = page.light_theme = ft.theme.Theme(
                color_scheme_seed=ft.colors.random_color()
            )

    def get_route_list(route):
        route_list = [item for item in route.split("/") if item != ""]
        return route_list

    def route_change(e):
        route_list = get_route_list(page.route)
        if len(route_list) == 0:
            page.go("/chat")
        else:
            gallery_view.display_control_examples(route_list[0])

    gallery_view = GalleryView(gallery)


    page.add(gallery_view)
    page.on_route_change = route_change
    page.go(page.route)


def init_config():
    # run_migrations()
    import os
    os.system("alembic revision --autogenerate -m \"Initial migration\"")
    os.system("alembic upgrade head")


if __name__ == '__main__':
    init_config()
    ft.app(main)