import flet as ft


class Message:
    def __init__(self, sender, content, plugins=None):
        self.sender = sender
        self.content = content
        self.plugins = plugins or []


class Plugin:
    def __init__(self, name, input_data, output_data):
        self.name = name
        self.input_data = input_data
        self.output_data = output_data
        self.is_loading = True
        self.show_details = False




class ChatDialog(ft.Column):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.messages = [
            Message(sender='user', content="Hi there! This is a test message."),
            Message(sender='assistant', content="Hello! I'm happy to help you."),
            Message(
                sender='user',
                content="How to write a quick sort in python?",
            ),
            Message(
                sender='assistant',
                content="""


# Flet

<img src="https://raw.githubusercontent.com/flet-dev/flet/flet-widget/media/logo/flet-logo.svg" width="50%"/>

Flet is a framework for adding server-driven UI (SDUI) experiences to existing Flutter apps or building standalone web, mobile and desktop apps with Flutter UI.

Add an interactive `FletApp` widget to your Flutter app whose content is controlled by a remote Python script.
It is an ideal solution for building non-core or frequently changing functionality such as product catalog, feedback form, in-app survey or support chat. Flet enables your team to ship new features faster by reducing the number of App Store validation cycles. Just re-deploy a web app hosting a Python script and your users will get an instant update!

On the server side Flet provides an easy to learn programming model that enables Python developers without prior Flutter (or even front-end) experience to participate in development of your larger Flutter app or build their own apps with Flutter UI from scratch.

## Getting started with Flet

### Install `flet` Python module

Flet requires Python 3.7 or above. To start with Flet, you need to install flet module first:

```
pip install flet
```

### Create Python program

Create a new Python program using Flet which will be driving the content of `FletApp` widget.

Let's do a simple `counter.py` app similar to a Flutter new project template:

```python
import flet
from flet import IconButton, Page, Row, TextField, icons

def main(page: Page):
    page.title = "Flet counter example"
    page.vertical_alignment = "center"

    txt_number = TextField(value="0", text_align="right", width=100)

    def minus_click(e):
        txt_number.value = int(txt_number.value) - 1
        page.update()

    def plus_click(e):
        txt_number.value = int(txt_number.value) + 1
        page.update()

    page.add(
        Row(
            [
                IconButton(icons.REMOVE, on_click=minus_click),
                txt_number,
                IconButton(icons.ADD, on_click=plus_click),
            ],
            alignment="center",
        )
    )

flet.app(target=main, port=8550)
```

Run the app:

```
python counter.py
```

You should see the app running in a native OS window.

There is a web server (Fletd) running in the background on a fixed port `8550`. Fletd web server is a "bridge" between Python and Flutter.

`FletApp` widget in your Flutter application will be communicating with Fletd web server via WebSockets to receive UI updates and send user-generated UI events.

For production use Python app along with Fletd could be [deployed to a public web host](https://flet.dev/docs/guides/python/deploying-web-app) and be accessible via HTTPS with domain name.

### Add Flet widget to a Flutter app

Create a new or open existing Flutter project.

Install Flutter `flet` package:

```
flutter pub add flet
```

For a new project replace `main.dart` with the following:

```dart
import 'package:flet/flet.dart';
import 'package:flutter/material.dart';

void main() async {
  await setupDesktop();
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      title: 'Flet Flutter Demo',
      home: FletApp(pageUrl: "http://localhost:8550"),
    );
  }
}
```

In the app above `FletApp` widget is hosted inside `MaterialApp` widget.

If Flet app must be able to handle page route change events (web browser URL changes, mobile app deep linking) it must be the top most widget as it contains its own `MaterialApp` widget handling route changes:

```dart
import 'package:flet/flet.dart';
import 'package:flutter/material.dart';

void main() async {
  await setupDesktop();
  runApp(const FletApp(pageUrl: "http://localhost:8550"));
}
```

Run the program and see Flet app running inside a Flutter app.

When adding `FletApp` widget to the existing desktop Flutter app make sure `setupDesktop()` is called before `runApp()` to initialize Flet's built-in window manager.

## Flet learning resources

* [Getting started for Python](https://flet.dev/docs/guides/python/getting-started/)
* [Controls reference](https://flet.dev/docs/controls)
* [Tutorials](https://flet.dev/docs/tutorials)
* [Examples](https://github.com/flet-dev/examples/tree/main/python)

## Flet community

* [Discussions](https://github.com/flet-dev/flet/discussions)
* [Discord](https://discord.gg/dzWXP8SHG8)
* [Twitter](https://twitter.com/fletdev)
* [Email](mailto:hello@flet.dev)

## FAQ

Coming soon.

## Adding custom Flutter widgets

Coming soon.
        """,
            ),

        ]
        self.list_view = ft.ListView(
            controls=[self.build_message(msg) for msg in self.messages],
            expand=True,
            auto_scroll=True,
            padding=0,
        )



        self.controls = [
            ft.Container(
                content=self.list_view,
                expand=True,
                padding=10,
            ),
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.IconButton(
                            icon=ft.icons.ATTACH_FILE,
                            tooltip="Attach file",
                            rotate=35
                        ),
                        ft.Container(
                            content=ft.TextField(
                                value="",
                                multiline=True,
                                min_lines=1,
                                border_radius=15,
                                border=ft.InputBorder.OUTLINE,
                                content_padding=ft.Padding(10, 10, 10, 10),
                            ),
                            expand=True
                        ),
                        ft.IconButton(
                            icon=ft.icons.SEND,
                            tooltip="Send"
                        )
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                ),
                padding=ft.padding.all(10)
            )
        ]
    def build_message(self, msg: Message):
        if msg.sender == 'user':
            avatar = ft.Icon(ft.icons.PERSON, size=40)
            # bubble_color = ft.colors.BLUE_100
        else:
            avatar = ft.Icon(ft.icons.AIR, size=40)
            # bubble_color = ft.colors.GREEN_100

        bubble_content = ft.Markdown(value=msg.content,
                                     selectable=True,
                                     extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                                     code_theme=ft.MarkdownCodeTheme.ATOM_ONE_DARK,
                                     code_style=ft.TextStyle(font_family="Roboto Mono"),
                                     on_tap_link=lambda e: self.page.launch_url(e.data),
                                     )
        bubble = ft.Container(
            content=bubble_content,
            padding=ft.padding.all(10),
            margin=ft.Margin(0,0,0,10),
            border=ft.Border(top=ft.BorderSide(1),left=ft.BorderSide(1),right=ft.BorderSide(1),bottom=ft.BorderSide(1)),
            border_radius=ft.border_radius.all(10),
            width=500,
        )

        if msg.sender == 'user':
            message_row = ft.Row(
                [
                    ft.Container(
                        content=bubble,
                        margin=ft.margin.symmetric(horizontal=10)
                    ),
                    avatar,
                ],
                alignment=ft.MainAxisAlignment.END,
                vertical_alignment=ft.CrossAxisAlignment.START,
                expand=True
            )
        else:
            message_row = ft.Row(
                [
                    avatar,
                    ft.Container(
                        content=bubble,
                        margin=ft.margin.symmetric(horizontal=10)
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.START,
                expand=True
            )

        # plugins_column = self.build_plugins_section(msg.plugins) if msg.plugins else None

        # if plugins_column:
        #     return ft.Column(
        #         [
        #             message_row,
        #             plugins_column
        #         ],
        #         expand=True
        #     )
        # else:
        return message_row
    # def build_plugins_section(self, plugins):
    #     plugin_controls = []
    #     for plugin in plugins:
    #         plugin_info_visibility = ft.Ref[ft.Row]
    #
    #         plugin_info_content = ft.Container(
    #             content=self.build_plugin_info(plugin),
    #             padding=ft.padding.only(left=20, top=5, bottom=5),
    #             visible=plugin.show_details,
    #         )
    #
    #         status_icon = ft.Icon(ft.icons.CIRCLE, size=16, rotate=0)
    #         if not plugin.is_loading:
    #             status_icon = ft.Icon(ft.icons.CHECK_CIRCLE, color=ft.colors.GREEN, size=16)
    #
    #         plugin_name_button = ft.TextButton(
    #             content=ft.Row(
    #                 [
    #                     status_icon,
    #                     ft.Text(value=plugin.name, color=ft.colors.BLUE, size=14)
    #                 ],
    #                 alignment=ft.MainAxisAlignment.START,
    #                 vertical_alignment=ft.CrossAxisAlignment.CENTER,
    #                 spacing=5
    #             ),
    #             on_click=lambda e, p=plugin: self.toggle_plugin_details(p)
    #         )
    #
    #         plugin_row = ft.Column(
    #             [
    #                 ft.Row(
    #                     [
    #                         plugin_name_button
    #                     ],
    #                     alignment=ft.MainAxisAlignment.START,
    #                     vertical_alignment=ft.CrossAxisAlignment.CENTER
    #                 ),
    #                 plugin_info_content
    #             ],
    #             alignment=ft.MainAxisAlignment.START,
    #             horizontal_alignment=ft.CrossAxisAlignment.START
    #         )
    #
    #         plugin_controls.append(plugin_row)
    #
    #         asyncio.create_task(self.simulate_plugin_loading(plugin))
    #
    #     return ft.Column(
    #         plugin_controls,
    #         spacing=5
    #     )
    # def build_plugin_info(self, plugin: Plugin):
    #     return ft.Column(
    #         [
    #             ft.Row([
    #                 ft.Text("插件名称:", weight=ft.FontWeight.BOLD),
    #                 ft.Text(plugin.name)
    #             ], spacing=5),
    #             ft.Row([
    #                 ft.Text("输入:", weight=ft.FontWeight.BOLD),
    #                 ft.Text(plugin.input_data)
    #             ], spacing=5),
    #             ft.Row([
    #                 ft.Text("输出:", weight=ft.FontWeight.BOLD),
    #                 ft.Text(plugin.output_data)
    #             ], spacing=5),
    #         ],
    #         spacing=5
    #     )
    # async def simulate_plugin_loading(self, plugin: Plugin):
    #     await asyncio.sleep(2)
    #     plugin.is_loading = False
    #     self.refresh_ui()
    #
    # def toggle_plugin_details(self, plugin: Plugin):
    #     plugin.show_details = not plugin.show_details
    #     self.refresh_ui()
    #
    # def refresh_ui(self):
    #     self.page.update()
    #
    # async def update_message_list(self):
    #     self.list_view.controls = [self.build_message(msg) for msg in self.messages]
    #     await self.list_view.update_async()
    #
    # def add_message(self, msg: Message):
    #     self.messages.append(msg)
    #     self.list_view.controls.append(self.build_message(msg))
    #     self.list_view.update()
    #     # 自动滚动到底部
    #     self.list_view.scroll_to(len(self.list_view.controls) - 1)
    #
    # def send_message(self, e):
    #     text_field = self.controls[1].content.controls[1].content
    #     content = text_field.value.strip()
    #     if content:
    #         user_msg = Message(sender='user', content=content)
    #         self.add_message(user_msg)
    #         text_field.value = ""
    #         self.controls[1].content.update()
    #
    #         assistant_reply = self.generate_assistant_reply(content)
    #         self.add_message(assistant_reply)
    #
    # def generate_assistant_reply(self, user_input):
    #     if "天气" in user_input:
    #         return Message(
    #             sender='assistant',
    #             content="好的，我来帮你查一下相关信息。",
    #             plugins=[
    #                 Plugin(name='天气插件', input_data='查询北京的天气', output_data='显示当前北京的天气信息')
    #             ]
    #         )
    #     else:
    #         return Message(sender='assistant', content="我不太明白您的意思，可以详细说明吗？")