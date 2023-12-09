import gc
from typing import Any, List

import pydantic
from typing import List, Optional

import torch
from pydantic import BaseModel, Field, HttpUrl


class BaseResponse(BaseModel):
    code: int = pydantic.Field(200, description="API status code")
    msg: str = pydantic.Field("success", description="API status message")
    data: Any = pydantic.Field(None, description="API data")

    class Config:
        schema_extra = {
            "example": {
                "code": 200,
                "msg": "success",
            }
        }


class ListResponse(BaseResponse):
    data: List[str] = pydantic.Field(..., description="List of names")

    class Config:
        schema_extra = {
            "example": {
                "code": 200,
                "msg": "success",
                "data": ["doc1.docx", "doc2.pdf", "doc3.txt"],
            }
        }


class Parameter(BaseModel):
    default: Optional[str] = ""
    in_: str = Field(..., alias='in')
    name: str
    description: str
    type_: str = Field(..., alias='type')
    required: bool


class Api(BaseModel):
    method: str
    optional_parameters: List[Parameter]
    test_endpoint: Any
    name: str
    description: str
    required_parameters: List[Parameter]
    url: HttpUrl


class Tool(BaseModel):
    tool_name: str
    api_list: List[Api]
    tool_description: str
    standardized_name: str
    title: str


class Project(BaseModel):
    project_name: str
    tools: List[Tool]


class Projects(BaseModel):
    projects: List[Project]


def torch_gc():
    try:
        if torch.cuda.is_available():
            # 删除模型和优化器的引用
            # 例如: del model, optimizer

            # 清空PyTorch的CUDA缓存
            torch.cuda.empty_cache()
            # 收集CUDA垃圾
            torch.cuda.ipc_collect()
            # 强制进行一次垃圾回收
            gc.collect()
        elif torch.backends.mps.is_available():
            try:
                from torch.mps import empty_cache
                empty_cache()
                gc.collect()
            except Exception as e:
                print("Error clearing MPS cache:", e)
    except Exception as e:
        print("An error occurred during torch_gc:", e)
