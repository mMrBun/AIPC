import asyncio
import importlib
import json
import os
import time
from typing import List
import importlib.util
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation import GenerationConfig
from configs import QWEN_MODEL_PATH

from core.decorator.class_decorator import singleton
from core.build_charts.format_echarts import EchartsBuilder
from core.build_tools.utils import extract_code
from .prompt.qwen_prompt_config import TOOL_DESC, PROMPT_REACT, ECHARTS_PROMPT



@singleton
class QwenFunctionCalling:
    def __init__(self):
        self.name = QWEN_MODEL_PATH
        self.tokenizer = AutoTokenizer.from_pretrained(self.name, trust_remote_code=True)
        self.generation_config = GenerationConfig.from_pretrained(self.name, trust_remote_code=True)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.name, device_map="auto", trust_remote_code=True
        ).eval()
        self.model.generation_config = self.generation_config
        self.model.generation_config.top_k = 1

    def llm_with_plugin(self, prompt: str, history, list_of_plugin_info, tools_callable_path):
        chat_history = [(x['user'], x['bot']) for x in history] + [(prompt, '')]

        # 需要让模型进行续写的初始文本
        planning_prompt = self.build_input_text(chat_history, list_of_plugin_info)

        text = ''
        last_observation = ""
        while True:
            output = self.text_completion(planning_prompt + text, stop_words=['Observation:', 'Observation:\n'])
            action, action_input, output = parse_latest_plugin_call(output)
            if action:  # 需要调用插件
                # thought, action_info, action_info_input = split_action(output)
                plugin_info = next(
                    ({"category": plugin.get("category_name"), "classification": plugin.get("name_for_human").lower()}
                     for plugin in list_of_plugin_info if plugin.get("name_for_model") == action), {})

                # action、action_input 分别为需要调用的插件代号、输入参数
                # observation是插件返回的结果，为字符串
                observation = call_plugin(action, action_input, tools_callable_path, plugin_info)
                last_observation = observation
                output += f'\nObservation: {observation}\nThought:'
                text += output
            else:  # 生成结束，并且不再需要调用插件
                text += output
                break

        new_history = []
        new_history.extend(history)
        new_history.append({'user': prompt, 'bot': text})
        chart_code = self.create_echarts_code(last_observation)
        return text, chart_code, new_history

    def create_echarts_code(self, observation):
        echarts_prompt = ECHARTS_PROMPT.format(
            observation=observation
        )
        output = self.model.chat(query=echarts_prompt, tokenizer=self.tokenizer, history=[])
        output = extract_code(output[0])
        output = json.loads(output)
        chart_type = output.get("chart_type")
        category = output.get("data").get("categories")
        data = output.get("data").get("series")
        chart_builder = EchartsBuilder(category, data)
        code = chart_builder.build_chart(chart_type)

        return code

    # 将对话历史、插件信息聚合成一段初始文本
    def build_input_text(self, chat_history, list_of_plugin_info) -> str:
        # 候选插件的详细信息
        tools_text = []
        for plugin_info in list_of_plugin_info:
            tool = TOOL_DESC.format(
                name_for_model=plugin_info["name_for_model"],
                name_for_human=plugin_info["name_for_human"],
                description_for_model=plugin_info["description_for_model"],
                parameters=json.dumps(plugin_info["parameters"], ensure_ascii=False),
                response=json.dumps(plugin_info["response"], ensure_ascii=False),
                # response_example=json.dumps(plugin_info["response_example"], ensure_ascii=False)
            )
            if plugin_info.get('args_format', 'json') == 'json':
                tool += " Format the arguments as a JSON object."
            elif plugin_info['args_format'] == 'code':
                tool += ' Enclose the code within triple backticks (`) at the beginning and end of the code.'
            else:
                raise NotImplementedError
            tools_text.append(tool)
        tools_text = '\n\n'.join(tools_text)

        # 候选插件的代号
        tools_name_text = ', '.join([plugin_info["name_for_model"] for plugin_info in list_of_plugin_info])

        im_start = '<|im_start|>'
        im_end = '<|im_end|>'
        prompt = f'{im_start}system\nYou are a helpful assistant.{im_end}'
        for i, (query, response) in enumerate(chat_history):
            if list_of_plugin_info:  # 如果有候选插件
                # 倒数第一轮或倒数第二轮对话填入详细的插件信息，但具体什么位置填可以自行判断
                if (len(chat_history) == 1) or (i == len(chat_history) - 2):
                    query = PROMPT_REACT.format(
                        tools_text=tools_text,
                        tools_name_text=tools_name_text,
                        query=query
                    )
            query = query.lstrip('\n').rstrip()  # 重要！若不 strip 会与训练时数据的构造方式产生差异。
            response = response.lstrip('\n').rstrip()  # 重要！若不 strip 会与训练时数据的构造方式产生差异。
            # 使用续写模式（text completion）时，需要用如下格式区分用户和AI：
            prompt += f"\n{im_start}user\n{query}{im_end}"
            prompt += f"\n{im_start}assistant\n{response}{im_end}"

        assert prompt.endswith(f"\n{im_start}assistant\n{im_end}")
        prompt = prompt[: -len(f'{im_end}')]
        return prompt

    def text_completion(self, input_text: str, stop_words) -> str:  # 作为一个文本续写模型来使用
        im_end = '<|im_end|>'
        if im_end not in stop_words:
            stop_words = stop_words + [im_end]
        stop_words_ids = [self.tokenizer.encode(w) for w in stop_words]

        input_ids = torch.tensor([self.tokenizer.encode(input_text)]).to(self.model.device)
        output = self.model.generate(input_ids, stop_words_ids=stop_words_ids)
        output = output.tolist()[0]
        output = self.tokenizer.decode(output, errors="ignore")
        assert output.startswith(input_text)
        output = output[len(input_text):].replace('<|endoftext|>', '').replace(im_end, '')

        for stop_str in stop_words:
            idx = output.find(stop_str)
            if idx != -1:
                output = output[: idx + len(stop_str)]
        return output  # 续写 input_text 的结果，不包含 input_text 的内容

    def do_chat(self, query: str, history: List[dict], top_p, temperature, tools_description_path, tools_callable_path):
        tools_description_path = format_qwen_tools_schema(tools_description_path)
        if len(history) > 1:
            history = history[-1:]
        print(f"User's Query:\n{query}\n")
        response, code, history = self.llm_with_plugin(prompt=query,
                                                       history=history,
                                                       list_of_plugin_info=tools_description_path,
                                                       tools_callable_path=tools_callable_path)
        return response, code,  history


def parse_latest_plugin_call(text):
    plugin_name, plugin_args = '', ''
    i = text.rfind('\nAction:')
    j = text.rfind('\nAction Input:')
    k = text.rfind('\nObservation:')
    if 0 <= i < j:  # If the text has `Action` and `Action input`,
        if k < j:  # but does not contain `Observation`,
            # then it is likely that `Observation` is ommited by the LLM,
            # because the output text may have discarded the stop word.
            text = text.rstrip() + '\nObservation:'  # Add it back.
        k = text.rfind('\nObservation:')
        plugin_name = text[i + len('\nAction:'): j].strip()
        plugin_args = text[j + len('\nAction Input:'): k].strip()
        text = text[:k]
    return plugin_name, plugin_args, text


def call_plugin(plugin_name: str, plugin_args: str, tools_callable_path, plugin_info) -> str:
    try:
        query = json.loads(plugin_args)
        query = {k.lower(): v for k, v in query.items()}
        module_path = os.path.join(tools_callable_path, plugin_info['category'], plugin_info['classification'],
                                   'api.py')
        spec = importlib.util.spec_from_file_location("api", module_path)
        api_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(api_module)
        func = getattr(api_module, plugin_name)
        return json.dumps(func(**query), ensure_ascii=False)
    except Exception as e:
        print(e)
        return ""


def format_qwen_tools_schema(list_of_plugin_info):
    new_list_of_plugin_info = []
    for item in list_of_plugin_info:
        item['name_for_human'] = item.pop('tool_name')
        item['name_for_model'] = item.pop('api_name')
        item['description_for_model'] = item.pop('api_description')
        item['parameters'] = []
        item['response'] = []
        required_parameters = item.pop('required_parameters')
        optional_parameters = item.pop('optional_parameters')
        for param in required_parameters:
            param_entity = {
                "name": param.get("name"),
                "type": param.get("type"),
                "description": param.get("description"),
                "required": True
            }
            item['parameters'].append(param_entity)
        for param in optional_parameters:
            param_entity = {
                "name": param.get("name"),
                "type": param.get("type"),
                "description": param.get("description"),
                "required": False
            }
            item['parameters'].append(param_entity)

        new_list_of_plugin_info.append(item)

    return new_list_of_plugin_info


def split_action(output):
    # 利用split方法分割字符串
    parts = output.split('\n')

    # 分割后的部分应该恰好是三个，否则输入格式可能错误
    if len(parts) != 3:
        raise ValueError("Input does not contain three parts separated by newlines.")

    # 分别提取Thought, Action, 和 Action Input
    thought = parts[0]
    action = parts[1]
    action_input = parts[2]

    return thought, action, action_input
