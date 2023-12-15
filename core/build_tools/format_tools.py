from fastapi import Body

from core.build_tools.utils import *
from core.utils import Projects, BaseResponse


def build_tools(
        tools_info: Projects = Body(..., description="api信息")
) -> BaseResponse:
    try:
        if isinstance(tools_info, str):
            tools_info = json.loads(tools_info)
            tools_info = Projects(**tools_info)
        projects = tools_info.projects
        for project in projects:
            project_name = camel_to_snake(project.project_name)

            # 解析接口文档
            categorized_apis_list, tag_list = format_swagger_doc(project)

            # 生成接口调用脚本
            process_api_doc_list(categorized_apis_list, project_name)

            # 生成tsv记录
            add_api_to_tsv(categorized_apis_list, project_name)

            # 生成json配置文件
            add_api_to_json(project_name, tag_list, categorized_apis_list)

        return BaseResponse(code=200, msg="工具初始化成功", data=[])
    except Exception as e:
        return BaseResponse(code=500, msg=f"工具初始化失败，错误信息:{e}", data=[])