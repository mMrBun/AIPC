import importlib
import json
import os
import re
import shutil
import string
import tempfile

from configs import BASE_PATH, MODEL_INIT_CONFIG


def format_swagger_doc(json_data):
    """
    @param json_data: 项目接口路由地址
    @return: 返回全部分类以及分类下的api
    """

    tag_list = []
    for item in json_data.tools:
        data = {
            "name": item.tool_name.replace(" ", "_").replace("-", "_"),
            "description": item.tool_description,
            "standardized_name": item.standardized_name
        }
        tag_list.append(data)
    categorized_apis = {}

    # 遍历paths字典拿到每个子字典做二次遍历
    for tool in json_data.tools:
        tag = tool.tool_name.replace(" ", "_").replace("-", "_")  # tag只可能有一个,相当于swagger文档中的分类标题
        for api in tool.api_list:
            if tag not in categorized_apis:
                categorized_apis[tag] = []
            categorized_apis[tag].append({
                'name': api.name,
                'method': api.method.upper(),
                'path': api.url,
                'summary': api.description,
                'parameters': {
                    "required_parameters": api.required_parameters,
                    "optional_parameters": api.optional_parameters
                },
                'responses': api.test_endpoint,
                "template_response": api.template_response if 'template_response' in api else None
            })

    # 推导式categorized_apis字典转list
    categorized_apis_list = [{'category': category, 'apis': apis} for category, apis in categorized_apis.items()]

    return categorized_apis_list, tag_list


def generate_params(params, required=True):
    header_params = [param.name for param in params if param.in_.lower() == 'header']
    query_params = [param.name for param in params if param.in_.lower() == 'query']
    header_params_str = generate_param_str(header_params, required)
    query_params_str = generate_param_str(query_params, required)
    return header_params_str, query_params_str, header_params, query_params


def generate_param_str(params, required=True):
    if required:
        return ', '.join([re.sub('-', '_', param.lower()) for param in params]) + ', ' if params else ''
    else:
        return ', '.join([f"{re.sub('-', '_', param.lower())}=None" for param in params]) + ', ' if params else ''


def generate_dict(params, other_params=[], required=True):
    param_list = [f'"{param}": {re.sub("-", "_", param.lower())}' for param in params]
    if not required:
        param_list += [f'"{param}": {param.lower() if param else "None"}' for param in other_params]
    return ', '.join(param_list)


def process_api_doc_list(api_list: list, project_name: str):
    """
    根据接口列表生成ToolLlaMa格式的配置文件
    @param api_list: 格式化后的接口列表
    @param project_name: 项目名称
    """
    target_path = os.path.join(BASE_PATH, 'functions', f'toolenv/tools', project_name)
    os.makedirs(target_path, exist_ok=True)

    for category in api_list:
        category_name = camel_to_snake(category['category'])
        category_path = os.path.join(target_path, category_name)
        os.makedirs(category_path, exist_ok=True)

        api_file_content = "import requests\n"
        api_file_content += "import json\n"
        for api in category['apis']:
            api_method = api['method']
            api_path = api['path']
            api_summary = api['summary']
            api_parameters = api['parameters']
            api_name = api['name']

            req_header_params_str, req_query_params_str, req_header_params, req_query_params = generate_params(api_parameters['required_parameters'])
            opt_header_params_str, opt_query_params_str, opt_header_params, opt_query_params = generate_params(api_parameters['optional_parameters'], required=False)

            optional_params_check = "\n".join([f"    if {re.sub('-', '_', param.lower())} is not None:\n        request_params['{param}'] = {re.sub('-', '_', param.lower())}" for param in opt_query_params])

            api_file_content += f"""
# {api_summary.split('/')[-1]}
def {camel_to_snake(api_name)}({req_header_params_str}{req_query_params_str}{opt_header_params_str}{opt_query_params_str}):
    url = "{api_path}"
    headers = {{ 
        {generate_dict(req_header_params, opt_header_params)}
    }}
    request_params = {{
        {generate_dict(req_query_params)}
    }}
{optional_params_check}
    response = requests.{api_method.lower()}(url, headers=headers, params=request_params)
    return json.loads(response.text)
"""
        api_file_path = os.path.join(category_path, "api.py")
        with open(api_file_path, 'w', encoding='utf-8') as api_file:
            api_file.write(api_file_content)

        print(f"API written to {api_file_path}")


def add_api_to_tsv(api_list, project_name):
    count = 1
    target_path = os.path.join(BASE_PATH, 'functions', f'retrieval/G1/', 'corpus.tsv')
    if not os.path.exists(target_path):
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        if not os.path.exists(target_path):
            with open(target_path, 'a', encoding='utf-8') as file:
                pass  # 空语句，不写入内容
            print(f"File '{target_path}' created.")
        else:
            print(f"File '{target_path}' already exists. Skipping creation.")

    with open(target_path, 'r', encoding='utf-8') as file:
        file_content = file.read()

    if file_content.strip():  # file content not null
        with open(target_path, 'a', encoding='utf-8') as file:
            last_count = get_last_count(target_path)
            count = last_count + 1
            write_to_tsv(
                api_list=api_list,
                count=count,
                file=file,
                project_name=project_name
            )

    else:  # file content null
        with open(target_path, 'w', encoding='utf-8') as file:
            file.write("docid\tdocument_content" + '\n')
            write_to_tsv(
                api_list=api_list,
                count=count,
                file=file,
                project_name=project_name
            )


def add_api_to_json(project_name, tags, api_list):
    target_path = os.path.join(BASE_PATH, 'functions', f'toolenv/tools', project_name)
    for tag in tags:
        api_demo_json = {
            "tool_description": tag['description'],
            "tool_name": tag['name'],
            "title": tag['name'],
            "api_list": [],
            "standardized_name": tag['standardized_name']
        }
        for tool in api_list:
            if tool['category'] != tag['name']:
                continue
            for api in tool['apis']:
                if api['method'].upper() != 'GET':
                    continue
                api_info = {
                    "name": camel_to_snake(api['name']),
                    "url": str(api['path']),
                    "description": api['summary'].split('/')[-1],
                    "method": api['method'].upper(),
                    "required_parameters": [],
                    "optional_parameters": [],
                    "test_endpoint": api['responses']
                }
                req_params = api['parameters']['required_parameters']
                opt_params = api['parameters']['optional_parameters']
                for req_param in req_params:
                    api_info['required_parameters'].append(
                        {
                            "name": re.sub("-", "_", req_param.name),
                            "type": req_param.type_,
                            "description": req_param.description,
                            "default": req_param.default
                        }
                    )
                for opt_param in opt_params:
                    api_info['optional_parameters'].append(
                        {
                            "name": re.sub("-", "_", opt_param.name),
                            "type": opt_param.type_,
                            "description": opt_param.description,
                            "default": opt_param.default
                        }
                    )
                api_demo_json['api_list'].append(api_info)  # 将api_info添加到api_list中

        # 创建project_name.json文件并写入api_demo_json内容
        # json_file_path = os.path.join(target_path, f"aaa.json")
        json_file_path = os.path.join(target_path, f"{tag['name'].lower()}.json")
        try:

            with open(json_file_path, 'w', encoding='utf-8') as json_file:
                json.dump(api_demo_json, json_file, indent=4, ensure_ascii=False)  # 格式化写入，缩进为4个空格
        except Exception as e:
            print(e)


def camel_to_snake(name):
    # 使用正则表达式将驼峰命名转换为下划线命名
    name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name)
    name = re.sub('-', '_', name)
    name = re.sub(' ', '_', name)
    return name.lower()


def write_to_tsv(api_list, count, file, project_name):
    for tool in api_list:
        for api in tool['apis']:
            api_method = api['method']
            if api_method.upper() != 'GET':
                continue
            api_path = str(api['path'])
            api_name = api['name']
            api_summary = api['summary']
            api_parameters = api['parameters']
            req_params = api_parameters['required_parameters']
            opt_params = api_parameters['optional_parameters']
            template_response = api['template_response']
            req_param_list = []
            opt_param_list = []
            tr_list = {f"\"\"{key}\"\"": f"\"\"{value}\"\"" for key, value in
                       template_response.items()} if template_response is not None else {}

            for req_param in req_params:
                req_param_list.append(
                    f"""{{""name"": ""{re.sub("-", "_", req_param.name)}"", ""type"": ""{req_param.type_}"", ""description"": ""{req_param.description}"", ""default"": ""null""}}""")

            for opt_param in opt_params:
                opt_param_list.append(
                    f"""{{""name"": ""{re.sub("-", "_", opt_param.name)}"", ""type"": ""{opt_param.type_}"", ""description"": ""{opt_param.description}"", ""default"": ""null""}}""")

            record = f"""{count}\t"{{""category_name"": ""{project_name}"",""tool_name"": ""{tool['category']}"",""api_name"": ""{camel_to_snake(api_name)}"",""api_description"": ""{remove_punctuation(api_summary.split('/')[-1])}"",""required_parameters"": {[', '.join(req_param_list)]},""optional_parameters"": {[', '.join(opt_param_list)]},""method"": ""{api_method.upper()}"",""template_response"":{tr_list}}}\""""
            file.write(record.replace("'", "") + '\n')
            count += 1


def get_last_count(target_path):
    last_line = None
    with open(target_path, 'r', encoding='utf-8') as file:
        for line in file:
            last_line = line
    if last_line:
        tag = last_line.split('\t')[0]
        if isinstance(tag, int):
            last_count = int(tag)
            return last_count
        else:
            return 0
    else:
        return 0


def remove_punctuation(inp_string):
    translator = inp_string.maketrans('', '', string.punctuation)
    no_punct_string = inp_string.translate(translator)
    return no_punct_string


def get_tsv_callable_path():
    tsv_path = os.path.join(BASE_PATH, "functions/retrieval/G1/corpus.tsv")
    tool_root_dir = os.path.join(BASE_PATH, "functions/toolenv/tools")
    return tsv_path, tool_root_dir


def get_model_class(model_type):
    """
    根据提供的模型类型，从MODEL_INIT_CONFIG获取类的路径，
    导入并返回类本身。

    :param model_type: 要获取的模型类型的名称
    :return: 对应的类，如果找不到则返回None
    """
    class_path = MODEL_INIT_CONFIG.get(model_type)
    if not class_path:
        raise ValueError(f"Model type '{model_type}' is not defined in MODEL_INIT_CONFIG.")

    # 分割模块路径和类名
    module_name, class_name = class_path.rsplit('.', 1)

    # 导入模块
    module = importlib.import_module(module_name)

    # 获取并返回类
    return getattr(module, class_name)


def extract_code(text: str):
    try:
        pattern = r'```([^\n]*)\n(.*?)```'
        matches = re.findall(pattern, text, re.DOTALL)
        return matches[-1][1]
    except Exception as e:
        return None
