import importlib
import json
import os
import importlib.util

from core.decorator.class_decorator import singleton
from llms.chatglm3.client import get_client
from llms.chatglm3.prompt_template import create_system_prompt


@singleton
class ChatGLM3FunctionCalling:

    def __init__(self):

        self.client = get_client()
        self.last_observation = ""

    def model_chat(self, task_query, system_info, top_p, temperature, tools_callable_path, plugin_info):
        model_history = [system_info]
        model_response, model_history = self.client.generate_chat(task_query, history=model_history, top_p=top_p,
                                                                  temperature=temperature, role="user")
        return self.run_task(model_response, model_history, top_p, temperature, tools_callable_path, plugin_info)

    def run_task(self, model_response, model_history, top_p, temperature, tools_callable_path, plugin_info):
        if isinstance(model_response, dict):
            # done 更改工具调用位置

            # 导入工具类
            module_path = os.path.join(tools_callable_path, plugin_info['category'],
                                       plugin_info['classification'],
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
            self.last_observation = func_response
            result = json.dumps(func_response, ensure_ascii=False)
            model_response, model_history = self.client.generate_chat(result, history=model_history, top_p=top_p,
                                                                      temperature=temperature, role="observation")
            model_response, model_history = self.run_task(model_response, model_history, top_p, temperature,
                                                          tools_callable_path, plugin_info)
            return model_response, model_history
        else:
            return model_response, model_history

    def do_chat(self, query, history, top_p, temperature, tools_description_path, tools_callable_path):

        tools = self.client.format_glm_tools_schema(tools_description_path)
        tools_system_info = create_system_prompt(tools)
        response, history = self.model_chat(query, tools_system_info, top_p, temperature, tools_callable_path, tools)
        code = self.client.create_echarts_code(self.last_observation)
        return response, code, history
