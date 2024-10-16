import flet as ft

from .examples_view import ExamplesView
from .left_navigation_menu import LeftNavigationMenu


class GalleryView(ft.Row):
    def __init__(self, gallery):
        super().__init__()
        self.gallery = gallery
        self.left_nav = LeftNavigationMenu(gallery)
        self.examples_view = ExamplesView(gallery)
        self.expand = True
        self.spacing = 0
        self.controls = [
            self.left_nav,
            ft.VerticalDivider(width=1, trailing_indent=1),
            self.examples_view,
        ]

    def display_control_examples(self, control_group_name):
        self.examples_view.display(
            self.gallery.get_control(
                control_group_name
            )
        )
        self.page.update()
