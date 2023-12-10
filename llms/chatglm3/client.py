from __future__ import annotations

import json
from collections.abc import Iterable
import os
from typing import Any, Protocol, List

from huggingface_hub.inference._text_generation import TextGenerationStreamResponse, Token
import torch
from transformers import AutoModel, AutoTokenizer, AutoConfig

from configs import CHATGLM3_MODEL_PATH
from web_server.build_charts.format_echarts import EchartsBuilder
from .conversation import Conversation
from ..qwen.prompt.qwen_prompt_config import ECHARTS_PROMPT

TOOL_PROMPT = 'Answer the following questions as best as you can. You have access to the following core:'

MODEL_PATH = os.environ.get('MODEL_PATH', CHATGLM3_MODEL_PATH)
PT_PATH = os.environ.get('PT_PATH', None)
TOKENIZER_PATH = os.environ.get("TOKENIZER_PATH", MODEL_PATH)


def get_client() -> Client:
    client = HFClient(MODEL_PATH, TOKENIZER_PATH, PT_PATH)
    return client


class Client(Protocol):
    def generate_stream(self,
                        system: str | None,
                        tools: list[dict] | None,
                        history: list[Conversation],
                        **parameters: Any
                        ) -> Iterable[TextGenerationStreamResponse]:
        ...

    def generate_chat(self, query, history, top_p, temperature, role=None):
        ...

    def format_glm_tools_schema(self, list_of_plugin_info):
        ...

    def create_echarts_code(self, observation):
        ...


def stream_chat(self, tokenizer, query: str, history: list[tuple[str, str]] = None, role: str = "user",
                past_key_values=None, max_length: int = 8192, do_sample=True, top_p=0.8, temperature=0.8,
                logits_processor=None, return_past_key_values=False, **kwargs):
    from transformers.generation.logits_process import LogitsProcessor
    from transformers.generation.utils import LogitsProcessorList

    class InvalidScoreLogitsProcessor(LogitsProcessor):
        def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor) -> torch.FloatTensor:
            if torch.isnan(scores).any() or torch.isinf(scores).any():
                scores.zero_()
                scores[..., 5] = 5e4
            return scores

    if history is None:
        history = []
    if logits_processor is None:
        logits_processor = LogitsProcessorList()
    logits_processor.append(InvalidScoreLogitsProcessor())
    eos_token_id = [tokenizer.eos_token_id, tokenizer.get_command("<|user|>"),
                    tokenizer.get_command("<|observation|>")]
    gen_kwargs = {"max_length": max_length, "do_sample": do_sample, "top_p": top_p,
                  "temperature": temperature, "logits_processor": logits_processor, **kwargs}
    if past_key_values is None:
        inputs = tokenizer.build_chat_input(query, history=history, role=role)
    else:
        inputs = tokenizer.build_chat_input(query, role=role)
    inputs = inputs.to(self.device)
    if past_key_values is not None:
        past_length = past_key_values[0][0].shape[0]
        if self.transformer.pre_seq_len is not None:
            past_length -= self.transformer.pre_seq_len
        inputs.position_ids += past_length
        attention_mask = inputs.attention_mask
        attention_mask = torch.cat((attention_mask.new_ones(1, past_length), attention_mask), dim=1)
        inputs['attention_mask'] = attention_mask
    history.append({"role": role, "content": query})
    print("input_shape>", inputs['input_ids'].shape)

    input_sequence_length = inputs['input_ids'].shape[1]

    if max_length < input_sequence_length <= self.config.seq_length:
        yield "Current input sequence length {} exceeds sequence length set in generation parameters {}. The maximum model sequence length is {}. You may adjust the generation parameter to enable longer chat history.".format(
            input_sequence_length, max_length, self.config.seq_length
        ), history
        return

    if input_sequence_length > self.config.seq_length:
        yield "Current input sequence length {} exceeds maximum model sequence length {}. Unable to generate tokens.".format(
            input_sequence_length, self.config.seq_length
        ), history
        return

    for outputs in self.stream_generate(**inputs, past_key_values=past_key_values,
                                        eos_token_id=eos_token_id, return_past_key_values=return_past_key_values,
                                        **gen_kwargs):
        if return_past_key_values:
            outputs, past_key_values = outputs
        outputs = outputs.tolist()[0][len(inputs["input_ids"][0]):]
        response = tokenizer.decode(outputs)
        if response and response[-1] != "�":
            new_history = history
            if return_past_key_values:
                yield response, new_history, past_key_values
            else:
                yield response, new_history


class HFClient(Client):
    def __init__(self, model_path: str, tokenizer_path: str, pt_checkpoint: str | None = None, ):
        self.model_path = model_path
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_path, trust_remote_code=True)

        if pt_checkpoint is not None:
            config = AutoConfig.from_pretrained(model_path, trust_remote_code=True, pre_seq_len=128)
            self.model = AutoModel.from_pretrained(model_path, trust_remote_code=True, config=config)
            prefix_state_dict = torch.load(os.path.join(pt_checkpoint, "pytorch_model.bin"))
            new_prefix_state_dict = {}
            for k, v in prefix_state_dict.items():
                if k.startswith("transformer.prefix_encoder."):
                    new_prefix_state_dict[k[len("transformer.prefix_encoder."):]] = v
            print("Loaded from pt checkpoints", new_prefix_state_dict.keys())
            self.model.transformer.prefix_encoder.load_state_dict(new_prefix_state_dict)
        else:
            self.model = AutoModel.from_pretrained(model_path, trust_remote_code=True)

        self.model = self.model.to(
            'cuda' if torch.cuda.is_available() else
            'mps' if torch.backends.mps.is_available() else
            'cpu'
        ).eval()

    def generate_stream(self,
                        system: str | None,
                        tools: list[dict] | None,
                        history: list[Conversation],
                        **parameters: Any
                        ) -> Iterable[TextGenerationStreamResponse]:
        chat_history = [{
            'role': 'system',
            'content': system if not tools else TOOL_PROMPT,
        }]

        if tools:
            chat_history[0]['core'] = tools

        for conversation in history[:-1]:
            chat_history.append({
                'role': str(conversation.role).removeprefix('<|').removesuffix('|>'),
                'content': conversation.content,
            })

        query = history[-1].content
        role = str(history[-1].role).removeprefix('<|').removesuffix('|>')

        text = ''

        for new_text, _ in stream_chat(self.model,
                                       self.tokenizer,
                                       query,
                                       chat_history,
                                       role,
                                       **parameters,
                                       ):
            word = new_text.removeprefix(text)
            word_stripped = word.strip()
            text = new_text
            yield TextGenerationStreamResponse(
                generated_text=text,
                token=Token(
                    id=0,
                    logprob=0,
                    text=word,
                    special=word_stripped.startswith('<|') and word_stripped.endswith('|>'),
                )
            )

    def generate_chat(self, query, history, top_p, temperature, role="user"):
        return self.model.chat(tokenizer=self.tokenizer, top_p=top_p, temperature=temperature, query=query,
                               history=history, role=role)

    def format_glm_tools_schema(self, list_of_plugin_info):
        tools = []
        for item in list_of_plugin_info:
            # 创建新的JSON结构
            transformed_json = {
                "name": item["api_name"],
                "description": item["api_description"],
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }

            # 处理必需参数
            for param in item["required_parameters"]:
                # 在properties中添加参数
                transformed_json["parameters"]["properties"][param["name"]] = {
                    "description": param["description"]
                }
                # 在required列表中添加参数名
                transformed_json["parameters"]["required"].append(param["name"])

            # 处理可选参数
            for param in item["optional_parameters"]:
                # 在properties中添加参数
                transformed_json["parameters"]["properties"][param["name"]] = {
                    "description": param["description"]
                }
                # 可选参数不需要添加到required列表中
            tools.append(transformed_json)
        return tools

    def create_echarts_code(self, observation):
        echarts_prompt = ECHARTS_PROMPT.format(
            observation=observation
        )
        output = self.model.generate(query=echarts_prompt, tokenizer=self.tokenizer, history=[])
        output = json.loads(output)
        chart_type = output.get("chart_type")
        category = output.get("data").get("categories")
        data = output.get("data").get("series")
        chart_builder = EchartsBuilder(category, data)
        code = chart_builder.build_chart(chart_type)
        return code
