import importlib
import json
import os
import importlib.util
from llms.chatglm3.client import get_client

from llms.chatglm3.code_interpreter import main
from llms.chatglm3.prompt_template import create_prompt, create_system_prompt
from llms.chatglm3.utils import extract_code


class ChatGLM3FunctionCalling:

    def __init__(self, tools_callable_path: str, plugin_info: dict):

        self.client = get_client()
        self.tools_callable_path: str = tools_callable_path,
        self.plugin_info = plugin_info

    def model_chat(self, task_query, system_info):
        model_history = [system_info]
        model_response, model_history = self.client.generate_chat(task_query, history=model_history, role="user")
        return self.run_task(model_response, model_history)

    def run_task(self, model_response, model_history):
        if isinstance(model_response, dict):
            # done 更改工具调用位置

            # 导入工具类
            module_path = os.path.join(self.tools_callable_path, self.plugin_info['category'],
                                       self.plugin_info['classification'],
                                       'api.py')
            spec = importlib.util.spec_from_file_location("api", module_path)
            api_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(api_module)

            # 解析出api名称
            func = getattr(api_module, model_response.get("name"))
            # 解析出api参数
            param = model_response.get("parameters")
            # api调用
            func_response = func(**param)
            result = json.dumps(func_response, ensure_ascii=False)
            model_response, model_history = self.client.generate_chat(result, history=model_history, role="observation")
            model_response, model_history = self.run_task(model_response, model_history)
            return model_response, model_history
        else:
            return model_response, model_history

    def do_chat(self, query, top_p, temperature, top_k, tools_description_path, tools_callable_path):

        tools = self.client.format_glm_tools_schema(tools_description_path)
        tools_system_info = create_system_prompt(tools)
        response, history = self.model_chat(query, tools_system_info)
        # todo 分离code interpreter代码，使用pyEcharts构建图表代码
        prompt = create_prompt(response)
        response_code = main(top_p, temperature, prompt, self.client)
        code = extract_code(response_code)
        return code, response
