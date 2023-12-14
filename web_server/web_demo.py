import os
import re
import sys

import gradio as gr
import torch

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from web_server import build_tools
from web_server import function_calling
from web_server import torch_gc


def text_analysis(text, model_type, top_k, top_p, temperature):
    torch_gc()

    torch.cuda.empty_cache()

    response, code, history = function_calling(text, top_k, top_p, temperature, model_type)

    html = """
    <head>
      <title>Awesome-pyecharts</title>
      <script src="https://cdn.jsdelivr.net/npm/echarts@5.4.1/dist/echarts.min.js"></script>
    </head>

    <body>
      <div id="main" style="width: 600px;height:400px;"></div>
      <script>
        var myChart = echarts.init(document.getElementById("main"));

        var option = {echarts_code};

        myChart.setOption(option);
      </script>
    </body>
    """

    pattern = r'var option_([a-f0-9]{32}) = \{(.*?)\};'

    matches = re.findall(pattern, code, re.DOTALL)
    if matches:
        for match in matches:
            uid, value = match
            print(f"找到变量: option_{uid}，值为: {value}")
            html = html.replace("echarts_code", value)
    else:
        print("没有找到匹配的JS变量。")

    return response, f"""<iframe style="width: 100%; height: 480px" srcdoc='{html}'></iframe>"""


text_analysis_interface = gr.Interface(
    text_analysis,
    inputs=[
        gr.Textbox(placeholder="Enter sentence here..."),
        gr.Dropdown(["ChatGLM3效果太差了，建议使用Qwen", "Qwen"], label="模型类型", info="使用ChatGLM或Qwen"),
        gr.Slider(0, 10, 5, step=1, label="top_k", info="检索出多少个最相关的api信息"),
        gr.Slider(0.0, 1.0, 0.8, step=0.01, label="top_p"),
        gr.Slider(0.0, 1.5, 0.95, step=0.01, label="temperature")
    ],
    outputs=[gr.Textbox(), gr.HTML()],
    examples=[
        ["我们客户的年龄分布是怎么样的？"],
        ["我们产品的销售量怎么样？"],
        ["我们每个月销售额是多少？"]
    ],
)

# 创建一个新的接口，用于 JSON 数据输入和处理
json_interface = gr.Interface(
    build_tools,
    inputs=gr.Textbox(placeholder="Enter JSON here..."),
    outputs="text",
    live=False,
    examples=["""
        {
        "projects": [
            {
                "project_name": "财务类接口",
                "tools": [
                    {
                        "tool_name": "个人财务api",
                        "api_list": [
                            {
                                "method": "GET",
                                "optional_parameters": [],
                                "test_endpoint": {
                                    "1月": 569.23,
                                    "2月": 460.74,
                                    "3月": 541.36,
                                    "4月": 682.78,
                                    "5月": 159.35,
                                    "6月": 357.12,
                                    "7月": 852.46,
                                    "8月": 741.32,
                                    "9月": 369.54,
                                    "10月": 523.98,
                                    "11月": 412.69,
                                    "12月": 785.95
                                },
                                "name": "get_annual_bill",
                                "description": "获取个人支付宝年度账单",
                                "required_parameters": [
                                    {
                                        "default": "2023",
                                        "in": "Query",
                                        "name": "year",
                                        "description": "年份 e.g. 2022, 2023",
                                        "type": "string",
                                        "required": "true"
                                    }
                                ],
                                "url": "https://xxx"
                            }
                        ],
                        "tool_description": "个人财务相关api",
                        "standardized_name": "",
                        "title": "财务类接口"
                    }
                ]
            }
        ]
    }
    """

              ]
)

# 使用 TabbedInterface 将两个接口结合到一个界面中
demo = gr.TabbedInterface(
    [text_analysis_interface, json_interface],
    ["Text Analysis", "JSON Builder"]
)

if __name__ == '__main__':
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)
