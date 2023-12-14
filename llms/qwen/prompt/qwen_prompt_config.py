TOOL_DESC = """{name_for_model}: Call this tool to interact with the {name_for_human} API. What is the {name_for_human} API useful for? {description_for_model} Parameters: {parameters} Response: {response}"""

PROMPT_REACT = """Answer the following questions as best you can. You have access to the following APIs:

{tools_text}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tools_name_text}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can be repeated zero or more times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {query}"""

ECHARTS_PROMPT = """
Task：你的任务是返回json数据
Action：下面提供了三种图标的json格式，你需要将API返回的数据转换为其中的一种，其中type_name需要填充为当前数据主题，例如账单数据就是账单A，以此类推
Goal：只转换一种图表即可，请确保严格按照示例格式进行转换。
柱状图JSON Schema示例：
{{
"chart_type": "bar",
"data": {{
"categories": ["category1", "category2", "category3"],
"series": [
{{
"name": "type_name",
"data": [value1, value2, value3]
}}
]
}}
}}
饼图JSON Schema示例：
{{
"chart_type": "pie",
"data": {{
"series": [
{{"name": "category1", "value": value1}},
{{"name": "category2", "value": value2}},
{{"name": "category3", "value": value3}}
]
}}
}}
折线图JSON Schema示例：
{{
"chart_type": "line",
"data": {{
"categories": ["category1", "category2", "category3"],
"series": [
{{
"name": "type_name",
"data": [value1, value2, value3]
}}
]
}}
}}
API返回的数据：
{observation}
"""
