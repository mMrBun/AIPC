import json

from pyecharts.charts import Bar
from pyecharts.charts import Pie
from pyecharts.charts import Line


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
