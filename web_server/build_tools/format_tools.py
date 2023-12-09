import json

from fastapi import Body

from web_server.build_tools.utils import *
from web_server.utils import Projects, BaseResponse


def build_tools(
        tools_info: json = Body(..., description="工具数据")
) -> BaseResponse:
    try:
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


if __name__ == '__main__':
    json_info = """
    
    {
        "projects": [{
                "tenant_id": 210,
                "project_id": 348,
                "project_name": "口岸",
                "tools": [{
                        "tool_name": "出口退税大盘",
                        "api_list": [{
                                "method": "GET",
                                "optional_parameters": [],
                                "test_endpoint": {},
                                "name": "业务申报货值情况",
                                "description": "业务申报货值情况",
                                "required_parameters": [],
                                "url": "http://192.168.1.51:8080/wisdom-port-service/internationExpress/getBusinessDeclarationsGoodsValue"
                        }, {
                                "method": "GET",
                                "optional_parameters": [],
                                "test_endpoint": {},
                                "name": "本年度数据统计时间",
                                "description": "本年度数据统计时间",
                                "required_parameters": [],
                                "url": "http://192.168.1.51:8080/wisdom-port-service/internationExpress/statisticsTime"
                        }, {
                                "method": "GET",
                                "optional_parameters": [],
                                "test_endpoint": {},
                                "name": "当年业务贸易国家地区TOP5",
                                "description": "当年业务贸易国家地区TOP5",
                                "required_parameters": [],
                                "url": "http://192.168.1.51:8080/wisdom-port-service/internationExpress/getExpressTradeAreaStatTop5"
                        }],
                        "tool_description": "出口退税大盘",
                        "standardized_name": "",
                        "title": "出口退税大盘"
                }, {
                        "tool_name": "国际快件数据大盘",
                        "api_list": [{
                                "method": "GET",
                                "optional_parameters": [],
                                "test_endpoint": {
                                        "a": "aa"
                                },
                                "name": "aaa",
                                "description": "aaa",
                                "required_parameters": [{
                                        "default": "",
                                        "in": "Query",
                                        "name": "id",
                                        "description": "aa",
                                        "type": "string",
                                        "required": "true"
                                }],
                                "url": "http://192.168.1.51:8080/wisdom-port-service/internationExpress/getExpressTradeAreaStatTop5"
                        }],
                        "tool_description": "国际快件数据大盘",
                        "standardized_name": "",
                        "title": "国际快件数据大盘"
                }]
        }]
}
    
    """
    build_tools(json_info)