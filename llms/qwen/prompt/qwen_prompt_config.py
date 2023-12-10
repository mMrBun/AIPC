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
请根据给定的JSON Schema示例和API返回的数据，将其转化为一下示例中的一个JSON数据。
柱状图JSON Schema示例：
{
  "chart_type": "bar",
  "data": {
    "categories": ["category1", "category2", "category3"],
    "series": [
      {
        "name": "商家A",
        "data": [value1, value2, value3]
      }
    ]
  }
}
饼图JSON Schema示例：
{
  "chart_type": "pie",
  "data": {
    "series": [
      {"name": "category1", "value": value1},
      {"name": "category2", "value": value2},
      {"name": "category3", "value": value3}
    ]
  }
}
折线图JSON Schema示例：
{
  "chart_type": "line",
  "data": {
    "categories": ["category1", "category2", "category3"],
    "series": [
      {
        "name": "商家A",
        "data": [value1, value2, value3]
      }
    ]
  }
}
API返回的数据：
{observation}
请将上述API返回的数据转换为适合柱状图的JSON数据。
"""
