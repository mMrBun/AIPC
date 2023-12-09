import os
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

    response, history = function_calling(text, top_k, top_p, temperature, model_type)

    return response, None


text_analysis_interface = gr.Interface(
    text_analysis,
    inputs=[
        gr.Textbox(placeholder="Enter sentence here..."),
        gr.Dropdown(["ChatGLM3", "Qwen"], label="模型类型", info="使用ChatGLM或Qwen"),
        gr.Slider(0, 10, 5, step=1, label="top_k", info="检索出多少个最相关的api信息"),
        gr.Slider(0.0, 1.0, 0.8, step=0.01, label="top_p"),
        gr.Slider(0.0, 1.5, 0.95, step=0.01, label="temperature")
    ],
    outputs=[gr.Textbox(), gr.Plot()],
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
            "projects": [{
                "project_name": "接口测试",
                "tools": [{
                    "tool_name": "bbb",
                    "api_list": [{
                        "method": "GET",
                        "optional_parameters": [],
                        "test_endpoint": {},
                        "name": "www",
                        "description": "www",
                        "required_parameters": [],
                        "url": "https://xxx"
                    }, {
                        "method": "GET",
                        "optional_parameters": [],
                        "test_endpoint": {},
                        "name": "qqq",
                        "description": "qqq",
                        "required_parameters": [],
                        "url": "https://xxx"
                    }],
                    "tool_description": "出口退税大盘",
                    "standardized_name": "",
                    "title": "出口退税大盘"
                }, {
                    "tool_name": "aaa",
                    "api_list": [{
                        "method": "GET",
                        "optional_parameters": [],
                        "test_endpoint": {
                            "a": "aa"
                        },
                        "name": "aaa",
                        "description": "aaa",
                        "required_parameters": [{
                            "default": "",
                            "in": "Query",
                            "name": "id",
                            "description": "aa",
                            "type": "string",
                            "required": "true"
                        }],
                        "url": "https://xxx"
                    }],
                    "tool_description": "aaa",
                    "standardized_name": "",
                    "title": "aaa"
                }]
            }]
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
