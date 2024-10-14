import flet as ft

name = "Knowledgebase Page"
description = "Knowledgebase Page"

def build_page():
    # Sidebar
    sidebar = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(
                    content=ft.Image(src="path/to/profile_picture.png", width=50, height=50),
                    margin=ft.margin.only(bottom=20),
                ),
                ft.Text(value="Files", size=24, weight=ft.FontWeight.BOLD),
                ft.Text(value="Manage files and knowledge base", size=12),
                ft.Divider(),
                ft.ListView(
                    controls=[
                        ft.Text(value="All Files", size=16),
                        ft.Text(value="Documents", size=16),
                        ft.Text(value="Images", size=16),
                        ft.Text(value="Audio", size=16),
                        ft.Text(value="Videos", size=16),
                        ft.Divider(),
                        ft.Text(value="Knowledge Base", size=16, weight=ft.FontWeight.BOLD),
                        ft.Text(value="Twitter Marketing", size=16),
                        ft.Text(value="TailwindCSS", size=16),
                        ft.Text(value="Ant Design", size=16),
                        ft.Text(value="Python", size=16),
                        ft.Text(value="React", size=16),
                        ft.Text(value="Drizzle", size=16),
                        ft.Text(value="NextJS", size=16),
                    ],
                    expand=True
                )
            ],
            expand=True
        ),
        width=200,
        padding=ft.padding.all(10)
    )

    # File list header
    file_list_header = ft.Row(
        controls=[
            ft.TextField(hint_text="Search Files", expand=True),
            ft.IconButton(icon=ft.icons.UPLOAD),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )

    # File list
    file_list = ft.ListView(
        controls=[
            ft.Row(
                controls=[
                    ft.Text(value="index.html"),
                    ft.Text(value="a minute ago"),
                    ft.Text(value="0.3 KB"),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            ft.Row(
                controls=[
                    ft.Text(value="utils.ts"),
                    ft.Text(value="2 minutes ago"),
                    ft.Text(value="2.4 KB"),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            # Add more file rows here
        ],
        expand=True
    )

    # Main content area
    main_content = ft.Container(
        content=ft.Column(
            controls=[
                file_list_header,
                ft.Divider(),
                ft.Text(value="All Files", size=24, weight=ft.FontWeight.BOLD),
                ft.Text(value="Total 12 items"),
                file_list
            ],
            expand=True
        ),
        expand=True,
        padding=ft.padding.all(10),
    )

    return ft.Row(
            controls=[
                sidebar,
                main_content
            ],
            expand=True
        )