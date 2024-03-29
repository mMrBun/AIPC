"""
This is a tool based on langchain BaseTool class,
where you can define the input parameters and the implementation logic for the tool.
Please describe the parameters and the purpose of the tool in as much detail as possible,
as this can help the model work better.
"""
import abc
import json
from typing import Type, Any
from langchain.tools import BaseTool
from pydantic import BaseModel, Field

from server.extras.packages import is_pyecharts_available

if is_pyecharts_available():
    from pyecharts.charts import Bar
    from pyecharts.charts import Pie
    from pyecharts.charts import Line


class AnnualBillInput(BaseModel):
    year: str = Field(description="Year number", examples=[2023, 2024])
    chart_type: str = Field(description="图表类型，bar为柱状图，line为折线图，pie为饼图", examples=['bar', 'line', 'pie'])


class AnnualBill(BaseTool, abc.ABC):
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
    name = "get_annual_bill"
    description = "Get the annual bill for a given year and return a chart"
    args_schema: Type[BaseModel] = AnnualBillInput
    enabled = True

    def __init__(self):
        super().__init__()

    async def _arun(
            self,
            *args: Any,
            **kwargs: Any,
    ) -> Any:
        """
        Write down the implementation logic for the tool here.
        """
        bill = {
            "year": kwargs.get("year"),
            "bill": [
                {
                    "month": 1,
                    "cost": 100,
                },
                {
                    "month": 2,
                    "cost": 120,
                },
                {
                    "month": 3,
                    "cost": 90,
                },
                {
                    "month": 4,
                    "cost": 110,
                },
                {
                    "month": 5,
                    "cost": 130,
                },
                {
                    "month": 6,
                    "cost": 150,
                },
                {
                    "month": 7,
                    "cost": 140,
                },
                {
                    "month": 8,
                    "cost": 160,
                },
                {
                    "month": 9,
                    "cost": 170,
                },
                {
                    "month": 10,
                    "cost": 180,
                },
                {
                    "month": 11,
                    "cost": 190,
                },
                {
                    "month": 12,
                    "cost": 200,
                },
            ]
        }
        x_axis = [item.get("month") for item in bill.get("bill")]
        y_axis = [{"name": "cost", "data": [item.get("cost") for item in bill.get("bill")]}]
        echarts_builder = EchartsBuilder(x_axis=x_axis, y_axis=y_axis)
        chart_html_code = echarts_builder.build_chart(chart_type=kwargs.get("chart_type"))
        return chart_html_code


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
