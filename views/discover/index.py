import flet as ft

name = "Discover Page"
description = "Discover Page"

def build_page():
    # Top navigation bar
    nav_bar = ft.Row(
        controls=[
            ft.Text(value="LobeChat", size=24, weight=ft.FontWeight.BOLD),
            ft.TextField(hint_text="搜索名称介绍或关键词...", width=300),
            ft.IconButton(icon=ft.icons.CREATE)
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

    # Navigation menu
    nav_menu = ft.Row(
        controls=[
            ft.IconButton(icon=ft.icons.PERSON),
            ft.Text(value="助手"),
        ],
        alignment=ft.MainAxisAlignment.START,
    )

    # Helper card component
    def helper_card(title, author, date, description, category, icon):
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Text(value=title, size=18, weight=ft.FontWeight.BOLD),
                                ft.Icon(name=icon)
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                        padding=ft.padding.all(10),
                    ),
                    ft.Text(value=f"{author} {date}", size=12, color=ft.colors.BLACK12),
                    ft.Text(value=description, size=14),
                    ft.Row(
                        controls=[
                            ft.Icon(name=ft.icons.LABEL),
                            ft.Text(value=category, size=12)
                        ]
                    )
                ],
                alignment=ft.MainAxisAlignment.START,
                spacing=5
            ),
            width=300,
            height=200,
            padding=ft.padding.all(10),
            margin=ft.margin.all(5),
            border_radius=10,
            shadow=ft.BoxShadow(
                color=ft.colors.BLACK12,
                blur_radius=5,
                offset=ft.Offset(0, 2)
            )
        )

    helper_cards = ft.GridView(
        runs_count=5,
        max_extent=150,
        child_aspect_ratio=1.0,
        spacing=5,
        run_spacing=5,
        expand=True,
        controls=[
            helper_card("GitHub项目文档助手", "Luyi-2333", "2024-10-14", "专注开源项目文档编写与优化", "文案",
                        ft.icons.DESCRIPTION),
            helper_card("眼科医生", "yuphone", "2024-10-14", "擅长眼科诊断与治疗建议提供", "学术",
                        ft.icons.VISIBILITY),
            helper_card("半导体文本优化专家", "yuphone", "2024-10-14", "擅长半导体行业文本优化与规范化写作",
                        "文案", ft.icons.BUILD),
            helper_card("无线通信专家", "yuphone", "2024-10-14", "擅长无线通信技术，精通4G至6G的行业知识",
                        "学术", ft.icons.WIFI),
            helper_card("Xilinx FPGA方案专家", "yuphone", "2024-10-14", "擅长Xilinx FPGA方案设计与实现", "编程",
                        ft.icons.MEMORY),
            helper_card("健身专家", "Lockeysama", "2024-10-08", "知识渊博的健身专家", "生活",
                        ft.icons.FITNESS_CENTER),
            helper_card("代码优化/错误修改", "alphandbelt", "2024-10-08",
                        "精通多种编程语言，优化代码结构，修复错误并提供优雅的解决方案", "编程", ft.icons.CODE),
            helper_card("伦理安全分析师", "ayeantics", "2024-10-08",
                        "专注于识别和解决网络和移动平台中的安全漏洞。", "安全", ft.icons.LOCK),
            helper_card("GitHub项目文档助手", "Luyi-2333", "2024-10-14", "专注开源项目文档编写与优化", "文案",
                        ft.icons.DESCRIPTION),
            helper_card("眼科医生", "yuphone", "2024-10-14", "擅长眼科诊断与治疗建议提供", "学术",
                        ft.icons.VISIBILITY),
            helper_card("半导体文本优化专家", "yuphone", "2024-10-14", "擅长半导体行业文本优化与规范化写作",
                        "文案", ft.icons.BUILD),
            helper_card("无线通信专家", "yuphone", "2024-10-14", "擅长无线通信技术，精通4G至6G的行业知识",
                        "学术", ft.icons.WIFI),
            helper_card("Xilinx FPGA方案专家", "yuphone", "2024-10-14", "擅长Xilinx FPGA方案设计与实现", "编程",
                        ft.icons.MEMORY),
            helper_card("健身专家", "Lockeysama", "2024-10-08", "知识渊博的健身专家", "生活",
                        ft.icons.FITNESS_CENTER),
            helper_card("代码优化/错误修改", "alphandbelt", "2024-10-08",
                        "精通多种编程语言，优化代码结构，修复错误并提供优雅的解决方案", "编程", ft.icons.CODE),
            helper_card("伦理安全分析师", "ayeantics", "2024-10-08",
                        "专注于识别和解决网络和移动平台中的安全漏洞。", "安全", ft.icons.LOCK),
            helper_card("GitHub项目文档助手", "Luyi-2333", "2024-10-14", "专注开源项目文档编写与优化", "文案",
                        ft.icons.DESCRIPTION),
            helper_card("眼科医生", "yuphone", "2024-10-14", "擅长眼科诊断与治疗建议提供", "学术",
                        ft.icons.VISIBILITY),
            helper_card("半导体文本优化专家", "yuphone", "2024-10-14", "擅长半导体行业文本优化与规范化写作",
                        "文案", ft.icons.BUILD),
            helper_card("无线通信专家", "yuphone", "2024-10-14", "擅长无线通信技术，精通4G至6G的行业知识",
                        "学术", ft.icons.WIFI),
            helper_card("Xilinx FPGA方案专家", "yuphone", "2024-10-14", "擅长Xilinx FPGA方案设计与实现", "编程",
                        ft.icons.MEMORY),
            helper_card("健身专家", "Lockeysama", "2024-10-08", "知识渊博的健身专家", "生活",
                        ft.icons.FITNESS_CENTER),
            helper_card("代码优化/错误修改", "alphandbelt", "2024-10-08",
                        "精通多种编程语言，优化代码结构，修复错误并提供优雅的解决方案", "编程", ft.icons.CODE),
            helper_card("伦理安全分析师", "ayeantics", "2024-10-08",
                        "专注于识别和解决网络和移动平台中的安全漏洞。", "安全", ft.icons.LOCK),
            helper_card("GitHub项目文档助手", "Luyi-2333", "2024-10-14", "专注开源项目文档编写与优化", "文案",
                        ft.icons.DESCRIPTION),
            helper_card("眼科医生", "yuphone", "2024-10-14", "擅长眼科诊断与治疗建议提供", "学术",
                        ft.icons.VISIBILITY),
            helper_card("半导体文本优化专家", "yuphone", "2024-10-14", "擅长半导体行业文本优化与规范化写作",
                        "文案", ft.icons.BUILD),
            helper_card("无线通信专家", "yuphone", "2024-10-14", "擅长无线通信技术，精通4G至6G的行业知识",
                        "学术", ft.icons.WIFI),
            helper_card("Xilinx FPGA方案专家", "yuphone", "2024-10-14", "擅长Xilinx FPGA方案设计与实现", "编程",
                        ft.icons.MEMORY),
            helper_card("健身专家", "Lockeysama", "2024-10-08", "知识渊博的健身专家", "生活",
                        ft.icons.FITNESS_CENTER),
            helper_card("代码优化/错误修改", "alphandbelt", "2024-10-08",
                        "精通多种编程语言，优化代码结构，修复错误并提供优雅的解决方案", "编程", ft.icons.CODE),
            helper_card("伦理安全分析师", "ayeantics", "2024-10-08",
                        "专注于识别和解决网络和移动平台中的安全漏洞。", "安全", ft.icons.LOCK),
            helper_card("GitHub项目文档助手", "Luyi-2333", "2024-10-14", "专注开源项目文档编写与优化", "文案",
                        ft.icons.DESCRIPTION),
            helper_card("眼科医生", "yuphone", "2024-10-14", "擅长眼科诊断与治疗建议提供", "学术",
                        ft.icons.VISIBILITY),
            helper_card("半导体文本优化专家", "yuphone", "2024-10-14", "擅长半导体行业文本优化与规范化写作",
                        "文案", ft.icons.BUILD),
            helper_card("无线通信专家", "yuphone", "2024-10-14", "擅长无线通信技术，精通4G至6G的行业知识",
                        "学术", ft.icons.WIFI),
            helper_card("Xilinx FPGA方案专家", "yuphone", "2024-10-14", "擅长Xilinx FPGA方案设计与实现", "编程",
                        ft.icons.MEMORY),
            helper_card("健身专家", "Lockeysama", "2024-10-08", "知识渊博的健身专家", "生活",
                        ft.icons.FITNESS_CENTER),
            helper_card("代码优化/错误修改", "alphandbelt", "2024-10-08",
                        "精通多种编程语言，优化代码结构，修复错误并提供优雅的解决方案", "编程", ft.icons.CODE),
            helper_card("伦理安全分析师", "ayeantics", "2024-10-08",
                        "专注于识别和解决网络和移动平台中的安全漏洞。", "安全", ft.icons.LOCK),
            helper_card("GitHub项目文档助手", "Luyi-2333", "2024-10-14", "专注开源项目文档编写与优化", "文案",
                        ft.icons.DESCRIPTION),
            helper_card("眼科医生", "yuphone", "2024-10-14", "擅长眼科诊断与治疗建议提供", "学术",
                        ft.icons.VISIBILITY),
            helper_card("半导体文本优化专家", "yuphone", "2024-10-14", "擅长半导体行业文本优化与规范化写作",
                        "文案", ft.icons.BUILD),
            helper_card("无线通信专家", "yuphone", "2024-10-14", "擅长无线通信技术，精通4G至6G的行业知识",
                        "学术", ft.icons.WIFI),
            helper_card("Xilinx FPGA方案专家", "yuphone", "2024-10-14", "擅长Xilinx FPGA方案设计与实现", "编程",
                        ft.icons.MEMORY),
            helper_card("健身专家", "Lockeysama", "2024-10-08", "知识渊博的健身专家", "生活",
                        ft.icons.FITNESS_CENTER),
            helper_card("代码优化/错误修改", "alphandbelt", "2024-10-08",
                        "精通多种编程语言，优化代码结构，修复错误并提供优雅的解决方案", "编程", ft.icons.CODE),
            helper_card("伦理安全分析师", "ayeantics", "2024-10-08",
                        "专注于识别和解决网络和移动平台中的安全漏洞。", "安全", ft.icons.LOCK)
        ],
    )

    # Main content area
    main_content = ft.Container(
        content=ft.Column(
            controls=[
                nav_menu,
                ft.Divider(),
                ft.Text(value="推荐助手", size=24, weight=ft.FontWeight.BOLD),
                helper_cards
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=10,
        ),
        expand=True
    )

    return ft.Column(
            controls=[
                nav_bar,
                main_content
            ],
            expand=True
        )