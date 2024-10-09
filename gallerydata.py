import os
import sys
import flet as ft
import importlib.util
from pathlib import Path



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
        self.import_modules()

    def get_control_group(self, control_group_name):
        for control_group in self.control_groups:
            if control_group.name == control_group_name:
                return control_group

    def get_control(self, control_group_name):
        control_group = self.get_control_group(control_group_name)
        for grid_item in control_group.grid_items:
            if grid_item.id == control_group_name:
                return grid_item
        return control_group

    def list_example_files(self, control_group_dir):
        file_path = os.path.join(
            str(Path(__file__).parent), "views", control_group_dir
        )
        example_files = [f for f in os.listdir(file_path) if f in ['index.py']]
        return example_files

    def import_modules(self):
        for control_group_dir in self.control_groups:

            grid_item = GridItem(control_group_dir.name)

            for file in self.list_example_files(control_group_dir.name):
                file_name = os.path.join(control_group_dir.name, file)
                module_name = file_name.replace("/", ".").replace(".py", "")

                if module_name in sys.modules:
                    print(f"{module_name!r} already in sys.modules")
                else:
                    file_path = os.path.join(
                        str(Path(__file__).parent), "views", file_name
                    )

                    spec = importlib.util.spec_from_file_location(
                        module_name, file_path
                    )
                    module = importlib.util.module_from_spec(spec)
                    sys.modules[module_name] = module
                    spec.loader.exec_module(module)
                    print(f"{module_name!r} has been imported")
                    example_item = ExampleItem()
                    example_item.example = module.build_page

                    example_item.file_name = (
                        module_name.replace(".", "/") + ".py"
                    )
                    example_item.name = module.name
                    example_item.order = file[
                        :2
                    ]  # first 2 characters of example file name (e.g. '01')
                    grid_item.examples.append(example_item)
            grid_item.examples.sort(key=lambda x: x.order)
            control_group_dir.grid_items.append(grid_item)
            try:
                control_group_dir.grid_items.sort(key=lambda x: x.name)
            except:
                print(control_group_dir.name, control_group_dir.grid_items)
