import json
import re
import torch
import transformers
import transformers.models.llama.modeling_llama
from functools import partial
from functools import wraps


def process_retrieval_document(tools_list):
    ir_corpus = {}
    corpus2tool = {}
    for i, tool in enumerate(tools_list):
        struct = ((tool.get("function", "").get("name", "") or "")
                  + ", "
                  + (tool.get("function", "").get("description", "") or "")
                  + ", "
                  + (json.dumps(tool.get("function", "").get("parameters", "")) or "")
                  + ", "
                  + (tool.get("function", "").get("required", "") or ""))
        ir_corpus[i] = struct
        corpus2tool[struct] = tool
    return ir_corpus, corpus2tool


def singleton(cls):
    instances = {}

    @wraps(cls)
    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return wrapper
