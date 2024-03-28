"""
This is a tool based on langchain BaseTool class,
where you can define the input parameters and the implementation logic for the tool.
Please describe the parameters and the purpose of the tool in as much detail as possible,
as this can help the model work better.
"""
import abc
import json
from typing import Any
from pydantic import BaseModel, Field

from server.extras.packages import is_pyecharts_available
from langchain.tools import BaseTool

if is_pyecharts_available():
    from pyecharts.charts import Bar
    from pyecharts.charts import Pie
    from pyecharts.charts import Line


class BuildChartsInput(BaseModel):
    chart_type: str = Field(description="The type of charts", examples=['bar', 'line', 'pie'])
    x_axis: str = Field(description="x axis data, this parameter is null when chart_type is pie.",
                        examples=[['1月', '2月', '3月'], ['1季度', '2季度', '3季度', '4季度']])
    y_axis: str = Field(description="y axis data", examples=[[10, 20, 30, 40], [56.7, 78.9, 45.3]])


class BuildCharts(BaseTool, abc.ABC):
    """
    🤗name: The name of the tool may require specific prefix words like "get_" in the inference client of some models.
    Please adjust the naming format here accordingly based on the differences between models.
    🤗description: Please provide as clear a description as possible of the tool,
    detailing what it is used for, what problem it solves, and the scenarios in which it is used.
    This can increase the accuracy of model selection for the right tool.
    🤗args_schema: For the tool input parameters, if possible, please provide a description, examples,
     and default values for each parameter.
     🤗enabled: If the tool is enabled or not. If the tool is not enabled, it will not be available for use.
    """
    name = "build_charts"
    description = "Build a chart using the given data"
    enabled = True

    def __init__(self):
        super().__init__()

    def _run(self, chart_type, x_axis, y_axis) -> str:
        """
        Please provide a detailed description of the implementation logic of the tool.
        This can help the model understand the tool better and use it more accurately.
        """
        e_chart_builder = EchartsBuilder(x_axis, y_axis)
        return e_chart_builder.build_chart(chart_type)

    async def _arun(
            self,
            *args: Any,
            **kwargs: Any,
    ) -> Any:
        e_chart_builder = EchartsBuilder(kwargs.get("x_axis"), kwargs.get("y_axis"))
        return e_chart_builder.build_chart(kwargs.get("chart_type"))


class EchartsBuilder:
    def __init__(self, x_axis, y_axis):
        self.x_axis = x_axis
        self.y_axis = y_axis

    def build_chart(self, chart_type):
        if chart_type.lower() == "bar":
            return self.build_bar_chart()
        if chart_type.lower() == "line":
            return self.build_line_chart()
        if chart_type.lower() == "pie":
            return self.build_pie_chart()

    def build_bar_chart(self):
        bar = Bar()
        bar.add_xaxis(self.x_axis)
        for data in self.y_axis:
            bar.add_yaxis(data.get("name"), data.get("data"))
        return bar.render_embed()

    def build_line_chart(self):
        line = Line()
        line.add_xaxis(self.x_axis)
        for data in self.y_axis:
            line.add_yaxis(data.get("name"), data.get("data"))
        return line.render_embed()

    def build_pie_chart(self):
        pie = Pie()
        pie.add("", json_to_tuple_set(self.y_axis))
        return pie.render_embed()


def json_to_tuple_set(json_str: str):
    data = json.loads(json_str)

    if not isinstance(data, list):
        raise ValueError("JSON must represent a list of elements")

    tuple_list = [tuple(item) for item in data]

    return tuple_list
