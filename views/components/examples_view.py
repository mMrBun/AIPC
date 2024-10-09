import flet as ft


class ExamplesView(ft.Column):
    def __init__(self, gallery):
        super().__init__()
        self.gallery = gallery
        self.visible = False
        self.expand = True
        self.examples = ft.Column(expand=True, spacing=0)
        self.controls = [
            self.examples,
        ]

    def display(self, grid_item):
        self.visible = True
        self.examples.controls = []
        # self.control_name_text.value = grid_item.name
        # self.control_description.value = grid_item.description

        for example in grid_item.examples:
            self.examples.controls.append(
                ft.Container(
                    content=example.example(),
                    # clip_behavior=ft.ClipBehavior.NONE,
                    expand=True,
                ),
            )
