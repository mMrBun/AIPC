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

        return message_row