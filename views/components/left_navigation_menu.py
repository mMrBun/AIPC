import flet as ft
from views.style_const import NAV_COL_MAX_WIDTH, NAV_COL_MIN_WIDTH

class PopupColorItem(ft.PopupMenuItem):
    def __init__(self, color, name):
        super().__init__()
        self.content = ft.Row(
            controls=[
                ft.Icon(name=ft.icons.COLOR_LENS_OUTLINED, color=color),
                ft.Text(name),
            ],
        )
        self.on_click = self.seed_color_changed
        self.data = color

    def seed_color_changed(self, e):
        self.page.theme = self.page.dark_theme = ft.theme.Theme(
            color_scheme_seed=self.data
        )
        self.page.update()


class NavigationItem(ft.Container):
    def __init__(self, destination, item_clicked):
        super().__init__()
        self.ink = True
        self.padding = 10
        self.border_radius = 5
        self.destination = destination
        self.icon = destination.icon
        self.text = destination.label
        self.content = ft.Row([ft.Icon(self.icon), ft.Text(self.text)])
        self.on_click = item_clicked
        self.visible = destination.visible


class NavigationColumn(ft.Column):
    def __init__(self, gallery):
        super().__init__()
        self.expand = 6
        self.spacing = 0
        self.scroll = ft.ScrollMode.ALWAYS
        self.width = NAV_COL_MAX_WIDTH
        self.gallery = gallery
        self.selected_index = 0
        self.controls = self.get_navigation_items()

    def before_update(self):
        super().before_update()
        self.update_selected_item()

    def get_navigation_items(self):
        navigation_items = []
        for destination in self.gallery.control_groups:
            navigation_items.append(
                NavigationItem(destination, item_clicked=self.item_clicked)
            )
        return navigation_items

    def item_clicked(self, e):
        self.selected_index = e.control.destination.index
        self.update_selected_item()
        self.page.go(f"/{e.control.destination.name}")

    def update_selected_item(self):
        for item in self.controls:
            item.bgcolor = None
            item.content.controls[0].name = item.destination.icon
        self.controls[self.selected_index].bgcolor = ft.colors.SECONDARY_CONTAINER
        self.controls[self.selected_index].content.controls[0].name = self.controls[
            self.selected_index
        ].destination.selected_icon


class LeftNavigationMenu(ft.Column):
    def __init__(self, gallery):
        super().__init__()
        self.gallery = gallery
        self.rail = NavigationColumn(gallery=gallery)
        self.is_expanded = True
        self.dark_light_text = ft.Text("Light theme")
        self.settings_text = ft.Text("Settings")
        self.animate_size = ft.animation.Animation(duration=200)
        self.dark_light_icon = ft.IconButton(
            icon=ft.icons.BRIGHTNESS_2_OUTLINED,
            tooltip="Toggle brightness",
            on_click=self.theme_changed,
        )
        self.toggle_button = ft.IconButton(
            icon=ft.icons.ARROW_LEFT,
            tooltip="Toggle menu",
            on_click=self.toggle_menu,
        )

        self.sub_rail = ft.Column(
            expand=1,
            controls=[
                ft.Row(
                    controls=[
                        self.dark_light_icon,
                        self.dark_light_text,
                    ]
                ),
                ft.Row(
                    controls=[
                        ft.PopupMenuButton(
                            icon=ft.icons.SETTINGS,
                            items=[
                                ft.PopupMenuItem(
                                    icon=ft.icons.BOOK,
                                    text="KnowledgeBase Settings",
                                    on_click=self.menu_clicked
                                ),
                                ft.PopupMenuItem(),
                                ft.PopupMenuItem(
                                    icon=ft.icons.MODEL_TRAINING,
                                    text="Model Settings",
                                    on_click=self.menu_clicked
                                ),
                            ]
                        ),
                        self.settings_text
                    ]
                ),
            ],
            width=NAV_COL_MAX_WIDTH
        )

        self.controls = [
            self.rail,
            self.sub_rail,
            self.toggle_button,
        ]

    def toggle_menu(self, e):
        self.is_expanded = not self.is_expanded
        self.update_menu()
        self.page.update()

    def update_menu(self):
        if self.is_expanded:
            self.rail.width = NAV_COL_MAX_WIDTH
            self.sub_rail.width = NAV_COL_MAX_WIDTH
            self.dark_light_text.visible = True
            self.settings_text.visible = True
            self.toggle_button.icon = ft.icons.ARROW_LEFT
            for item in self.rail.controls:
                item.content.controls[1].visible = True
                item.content.controls[1].opacity = 1
        else:
            self.rail.width = NAV_COL_MIN_WIDTH
            self.sub_rail.width = NAV_COL_MIN_WIDTH
            self.dark_light_text.visible = False
            self.settings_text.visible = False
            self.toggle_button.icon = ft.icons.ARROW_RIGHT
            for item in self.rail.controls:
                item.content.controls[1].visible = False
                item.content.controls[1].opacity = 0

    def menu_clicked(self, e):
        if e.control.text == "KnowledgeBase Settings":
            e.page.go("/knowledgebase_settings")
        elif e.control.text == "Model Settings":
            e.page.go("/model_settings")

    def theme_changed(self, e):
        if self.page.theme_mode == ft.ThemeMode.LIGHT:
            self.page.theme_mode = ft.ThemeMode.DARK
            self.dark_light_text.value = "Dark theme"
            self.dark_light_icon.icon = ft.icons.BRIGHTNESS_HIGH
            self.page.theme = self.page.dark_theme = ft.theme.Theme(
                color_scheme_seed=ft.colors.random_color(),
            )
        else:
            self.page.theme_mode = ft.ThemeMode.LIGHT
            self.dark_light_text.value = "Light theme"
            self.dark_light_icon.icon = ft.icons.BRIGHTNESS_2
            self.page.theme = self.page.dark_theme = ft.theme.Theme(
                color_scheme_seed=ft.colors.random_color()
            )
        self.page.update()
