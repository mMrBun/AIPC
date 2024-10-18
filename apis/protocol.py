from enum import Enum, unique
from typing import Optional, Union, List, Literal

from pydantic.v1 import BaseModel


@unique
class Role(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    FUNCTION = "function"
    TOOL = "tool"

class ImageURL(BaseModel):
    url: str

class MultimodalInputItem(BaseModel):
    type: Literal["text", "image_url"]
    text: Optional[str] = None
    image_url: Optional[ImageURL] = None

class Function(BaseModel):
    name: str
    arguments: str

class FunctionCall(BaseModel):
    id: str
    type: Literal["function"] = "function"
    function: Function

class ChatMessage(BaseModel):
    role: Role
    content: Optional[Union[str, List[MultimodalInputItem]]] = None
    tool_calls: Optional[List[FunctionCall]] = None