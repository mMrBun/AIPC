import os
import importlib.util
from langchain_community.tools.convert_to_openai import format_tool_to_openai_tool
from langchain.tools import BaseTool

from configs.base_config import TOOLS_DIR


def collect_tool_classes(path: str):
    """
    Collect all the tool classes in the given path.
    """
    tool_class_list = []
    modules = os.listdir(path)
    for module in modules:
        module_path = os.path.join(path, module)
        if os.path.isdir(module_path):
            tool_class_list.extend(collect_tool_classes(module_path))
        elif module.endswith('.py'):
            spec = importlib.util.spec_from_file_location(module[:-3], module_path)
            tool_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(tool_module)
            for attribute_name in dir(tool_module):
                attribute = getattr(tool_module, attribute_name)
                if isinstance(attribute, type) and issubclass(attribute, BaseTool) and attribute is not BaseTool:
                    tool_class_list.append(attribute)
    return tool_class_list


def get_tools() -> tuple[dict, list]:
    """
    Get all the tools in the TOOLS_DIR.
    tools_dict: A dictionary of tools, where the key is the tool name and the value is the langchain tool.
    toos_list: A list of tool's description, where each tool is formatted as an OpenAI tool.
    """
    tools_dict = {}
    toos_list = []
    tool_classes = collect_tool_classes(TOOLS_DIR)
    tools = [tool_class() for tool_class in tool_classes]
    for tool in tools:
        tools_dict[tool.name] = tool
        tool_description = format_tool_to_openai_tool(tool)
        toos_list.append(tool_description)
    return tools_dict, toos_list
