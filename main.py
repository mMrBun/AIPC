import logging

import flet as ft

from components.gallery_view import GalleryView
from gallerydata import GalleryData

gallery = GalleryData()

logging.basicConfig(level=logging.INFO)


def main(page: ft.Page):
    page.title = "AIPC"

    page.fonts = {
        "Roboto Mono": "RobotoMono-VariableFont_wght.ttf",
        "RobotoSlab": "RobotoSlab[wght].ttf",
    }

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

    page.theme_mode = ft.ThemeMode.LIGHT
    page.on_error = lambda e: print("Page error:", e.data)

    page.add(gallery_view)
    page.on_route_change = route_change
    print(f"Initial route: {page.route}")
    page.go(page.route)


ft.app(main)
