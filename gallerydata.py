import flet as ft
from views.chat.index import build_page as chat_page
from views.discover.index import build_page as discover_page
from views.knowledgebase.index import build_page as knowledgebase_page
from views.knowledgebase_settings.index import build_page as knowledgebase_settings_page
from views.model_settings.index import build_page as model_settings_page



class GridItem:
    def __init__(self, _id):
        self.id = _id
        self.name = None
        self.examples = []
        self.description = None


class ExampleItem:
    def __init__(self):
        self.name = None
        self.file_name = None
        self.order = None
        self.example = None


class ControlGroup:
    def __init__(self, name, label, icon, selected_icon, index, visible=True):
        self.name = name
        self.label = label
        self.icon = icon
        self.selected_icon = selected_icon
        self.grid_items = []
        self.index = index
        self.visible = visible


class GalleryData:
    def __init__(self):

        self.control_groups = [
            ControlGroup(
                name="chat",
                label="Chat",
                icon=ft.icons.GRID_VIEW,
                selected_icon=ft.icons.GRID_VIEW_SHARP,
                index=0,
            ),
            ControlGroup(
                name="knowledgebase",
                label="KnowledgeBase",
                icon=ft.icons.MENU_SHARP,
                selected_icon=ft.icons.MENU_SHARP,
                index=1,
            ),
            ControlGroup(
                name="discover",
                label="Discover",
                icon=ft.icons.INFO_OUTLINED,
                selected_icon=ft.icons.INFO_SHARP,
                index=2,
            ),
            ControlGroup(
                name="knowledgebase_settings",
                label="KnowledgeBaseSettings",
                icon=ft.icons.INFO_OUTLINED,
                selected_icon=ft.icons.INFO_SHARP,
                index=3,
                visible=False
            ),
            ControlGroup(
                name="model_settings",
                label="ModelSettings",
                icon=ft.icons.INFO_OUTLINED,
                selected_icon=ft.icons.INFO_SHARP,
                index=4,
                visible=False
            )
        ]
        self.modules = {
            "chat": chat_page(),
            "knowledgebase": knowledgebase_page(),
            "discover": discover_page(),
            "knowledgebase_settings": knowledgebase_settings_page(),
            "model_settings": model_settings_page()
        }
