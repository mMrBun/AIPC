import json

from llms.chatglm3 import tools_system_info
from llms.chatglm3.client import get_client

from llms.chatglm3.code_interpreter import main
from llms.chatglm3.prompt_template import create_prompt
from llms.chatglm3.utils import extract_code

client = get_client()


def model_chat(task_query, system_info):
    model_history = [system_info]
    model_response, model_history = client.generate_chat(task_query, history=model_history, role="user")
    return run_task(model_response, model_history)


def run_task(model_response, model_history):
    if isinstance(model_response, dict):
        import tools.function_map as fm
        func = getattr(fm, model_response.get("name"))
        param = model_response.get("parameters")
        func_response = func(**param)
        result = json.dumps(func_response, ensure_ascii=False)
        model_response, model_history = client.generate_chat(result, history=model_history, role="observation")
        model_response, model_history = run_task(model_response, model_history)
        return model_response, model_history
    else:
        return model_response, model_history


def chat_process(query, top_p, temperature):
    response, history = model_chat(query, tools_system_info)
    prompt = create_prompt(response)
    response_code = main(top_p, temperature, prompt, client)
    code = extract_code(response_code)
    return code, response


