import os

from server.utils.get_current_platform import get_os

CURRENT_PLATFORM = get_os()
ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS_DIR = os.path.join(ROOT_PATH, 'tools')


# You can use other embedding models there, such as: bge-large-zh, m3e-large, text2vec-base-chinese.
RETRIEVAL_MODEL_PATH = "MrBun/ToolRetrieval_IR_bert_based_chinese"
RETRIEVAL_MODEL_ENABLED = False


JSON_FORMAT_PROMPT = (
    """, in a JSON format representing the kwargs (e.g. ```{"input": "hello world", "num_beams": 5}```)"""
)

TOOL_SYSTEM_PROMPT = (
    "You have access to the following tools:\n{tool_text}"
    "Use the following format if using a tool:\n"
    "```\n"
    "Action: tool name (one of [{tool_names}]).\n"
    "Action Input: the input to the tool{format_prompt}.\n"
    "```\n"
)

REACT_SYSTEM_PROMPT = (
    "Answer the following questions as best you can. You have access to the following APIs:\n{tool_text}\n"

    "Use the following format:\n"

    "Question: the input question you must answer\n"
    "Thought: you should always think about what to do\n"
    "Action: the action to take, should be one of [{tool_names}]\n"
    "Action Input: the input to the action{format_prompt}.\n"
    "Observation: the result of the action\n"
    "... (this Thought/Action/Action Input/Observation can be repeated zero or more times)\n"
    "Thought: I now know the final answer\n"
    "Final Answer: the final answer to the original input question\n"

    "Begin!"
)

CHATGLM3_SYSTEM_PROMPT = (
    "Answer the following questions as best as you can. You have access to the following tools:\n{tool_text}"
)
