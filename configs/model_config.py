import os

CHATGLM3_MODEL_PATH = "D:\\work\\models\\chatglm3-6b"

QWEN_MODEL_PATH = "/data/models/Qwen-7B-Chat/"

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RETRIEVE_MODEL_PATH = os.path.join(BASE_PATH, "retriever", "retriever_model")

MODEL_INIT_CONFIG = {
    "ChatGLM3": "llms.ChatGLM3FunctionCalling",
    "Qwen": "llms.QwenFunctionCalling"
}

VERSION = "v1.0.0"
