import json
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Literal, Optional, Sequence, Set, Tuple, Union

from configs.base_config import TOOL_SYSTEM_PROMPT, REACT_SYSTEM_PROMPT, JSON_FORMAT_PROMPT, CHATGLM3_SYSTEM_PROMPT

SLOTS = Sequence[Union[str, Set[str], Dict[str, str]]]


def parse_default_tool(tools: List[Dict[str, Any]]) -> Tuple[str, List[str]]:
    tool_text = ""
    tool_names = []
    for tool in tools:
        param_text = ""
        for name, param in tool["parameters"]["properties"].items():
            required = ", required" if name in tool["parameters"].get("required", []) else ""
            enum = ", should be one of [{}]".format(", ".join(param["enum"])) if param.get("enum", None) else ""
            items = (
                ", where each item should be {}".format(param["items"].get("type", "")) if param.get("items") else ""
            )
            param_text += "  - {name} ({type}{required}): {desc}{enum}{items}\n".format(
                name=name,
                type=param.get("type", ""),
                required=required,
                desc=param.get("description", ""),
                enum=enum,
                items=items,
            )

        tool_text += "> Tool Name: {name}\nTool Description: {desc}\nTool Args:\n{args}\n".format(
            name=tool["name"], desc=tool.get("description", ""), args=param_text
        )
        tool_names.append(tool["name"])

    return tool_text, tool_names


def default_tool_formatter(tools: List[Dict[str, Any]]):
    tool_text, tool_names = parse_default_tool(tools)
    return TOOL_SYSTEM_PROMPT.format(
        tool_text=tool_text, tool_names=", ".join(tool_names), format_prompt=JSON_FORMAT_PROMPT
    )


def react_tool_formatter(tools: List[Dict[str, Any]]):
    tool_text, tool_names = parse_default_tool(tools)
    return REACT_SYSTEM_PROMPT.format(
        tool_text=tool_text, tool_names=", ".join(tool_names), format_prompt=JSON_FORMAT_PROMPT
    )


def chatglm3_tool_formatter(tools: List[Dict[str, Any]]):
    tool_text, _ = parse_default_tool(tools)
    return CHATGLM3_SYSTEM_PROMPT.format(
        tool_text=tool_text
    )


def default_tool_extractor(content: str) -> Union[str, Tuple[str, str]]:
    regex = re.compile(r"Action:\s*([a-zA-Z0-9_]+).*?Action Input:\s*(.*)", re.DOTALL)
    action_match = re.search(regex, content)
    if not action_match:
        return content

    tool_name = action_match.group(1).strip()
    tool_input = action_match.group(2).strip().strip('"').strip("```")
    try:
        arguments = json.loads(tool_input)
    except json.JSONDecodeError:
        return content

    return tool_name, json.dumps(arguments, ensure_ascii=False)


def chatglm3_tool_extractor(content: str) -> Union[str, Tuple[str, str]]:
    tool_name = ""
    arguments = {}
    for response in content.split("<|assistant|>"):
        tool_name, arguments = response.split("\n", maxsplit=1)
        if not tool_name.strip():
            # TODO code interpreter implement
            return content
        else:
            arguments = "\n".join(arguments.split("\n")[1:-1])

            def tool_call(**kwargs):
                return kwargs

            arguments = eval(arguments)

    return tool_name.strip(), json.dumps(arguments, ensure_ascii=False)


@dataclass
class Formatter(ABC):
    slots: SLOTS = field(default_factory=list)
    tool_format: Optional[Literal["default", "react", "chatglm3"]] = None

    @abstractmethod
    def apply(self, **kwargs) -> SLOTS: ...

    def extract(self, content: str) -> Union[str, Tuple[str, str]]:
        raise NotImplementedError


@dataclass
class EmptyFormatter(Formatter):
    def __post_init__(self):
        has_placeholder = False
        for slot in filter(lambda s: isinstance(s, str), self.slots):
            if re.search(r"\{\{[a-zA-Z_][a-zA-Z0-9_]*\}\}", slot):
                has_placeholder = True

        if has_placeholder:
            raise ValueError("Empty formatter should not contain any placeholder.")

    def apply(self, **kwargs) -> SLOTS:
        return self.slots


@dataclass
class StringFormatter(Formatter):
    def __post_init__(self):
        has_placeholder = False
        for slot in filter(lambda s: isinstance(s, str), self.slots):
            if re.search(r"\{\{[a-zA-Z_][a-zA-Z0-9_]*\}\}", slot):
                has_placeholder = True

        if not has_placeholder:
            raise ValueError("A placeholder is required in the string formatter.")

    def apply(self, **kwargs) -> SLOTS:
        elements = []
        for slot in self.slots:
            if isinstance(slot, str):
                for name, value in kwargs.items():
                    if not isinstance(value, str):
                        raise RuntimeError("Expected a string, got {}".format(value))

                    slot = slot.replace("{{" + name + "}}", value, 1)
                elements.append(slot)
            elif isinstance(slot, (dict, set)):
                elements.append(slot)
            else:
                raise RuntimeError("Input must be string, set[str] or dict[str, str], got {}".format(type(slot)))

        return elements


@dataclass
class FunctionFormatter(Formatter):
    def __post_init__(self):
        has_name, has_args = False, False
        for slot in filter(lambda s: isinstance(s, str), self.slots):
            if "{{name}}" in slot:
                has_name = True
            if "{{arguments}}" in slot:
                has_args = True

        if not has_name or not has_args:
            raise ValueError("Name and arguments placeholders are required in the function formatter.")

    def apply(self, **kwargs) -> SLOTS:
        content = kwargs.pop("content")
        try:
            function = json.loads(content)
            name = function["name"]
            arguments = json.dumps(function["arguments"], ensure_ascii=False)
        except Exception:
            name, arguments = "", ""

        elements = []
        for slot in self.slots:
            if isinstance(slot, str):
                slot = slot.replace("{{name}}", name).replace("{{arguments}}", arguments)
                elements.append(slot)
            elif isinstance(slot, (dict, set)):
                elements.append(slot)
            else:
                raise RuntimeError("Input must be string, set[str] or dict[str, str], got {}".format(type(slot)))

        return elements


@dataclass
class ToolFormatter(Formatter):
    def __post_init__(self):
        if self.tool_format is None:
            raise ValueError("Tool format was not found.")

    def apply(self, **kwargs) -> SLOTS:
        content = kwargs.pop("content")
        try:
            tools = json.loads(content)
            if not len(tools):
                return [""]

            if self.tool_format == "default":
                return [default_tool_formatter(tools)]
            elif self.tool_format == "react":
                return [react_tool_formatter(tools)]
            elif self.tool_format == "chatglm3":
                return [chatglm3_tool_formatter(tools)]
            else:
                raise NotImplementedError
        except Exception:
            return [""]

    def extract(self, content: str) -> Union[str, Tuple[str, str]]:
        if self.tool_format == "default" or self.tool_format == "react":
            return default_tool_extractor(content)
        elif self.tool_format == "chatglm3":
            return chatglm3_tool_extractor(content)
        else:
            raise NotImplementedError


@dataclass
class MessageFormatter(Formatter):
    def __post_init__(self):
        if self.tool_format is None:
            raise ValueError("Tool format was not found.")

    def apply(self, **kwargs) -> SLOTS:
        content = kwargs.pop("content")
        try:
            if self.tool_format == "default" or self.tool_format == "chatglm3":
                return content
            elif self.tool_format == "react":
                return f"\nObservation: {content}"
            else:
                raise NotImplementedError
        except Exception:
            return [""]
