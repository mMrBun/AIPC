import re

import gradio as gr
from matplotlib import pyplot as plt
from llms.chatglm3.generate import chat_process


def text_analysis(text, top_p, temperature):

    code, response = chat_process(text, top_p, temperature)

    locals_dict = {}

    modified_code = re.sub(r'plt\.figure\([^)]*\)', r'fg = \g<0>', code)

    exec(modified_code, {'plt': plt}, locals_dict)

    fg = locals_dict.get('fg')

    return response, fg


demo = gr.Interface(
    text_analysis,
    inputs=[
        gr.Textbox(placeholder="Enter sentence here..."),
        gr.Slider(0.0, 1.0, 0.8, step=0.01, label="top_p"),
        gr.Slider(0.0, 1.5, 0.95, step=0.01, label="temperature")
    ],
    outputs=[gr.Markdown(), gr.Plot()],
    examples=[
        ["我们客户的年龄分布是怎么样的？"],
        ["我们产品的销售量怎么样？"],
        ["我们每个月销售额是多少？"]
    ],
)

if __name__ == '__main__':
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)
