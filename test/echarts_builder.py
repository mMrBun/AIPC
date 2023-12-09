from pyecharts.charts import Bar


class EchartsBuilder:
    def __init__(self, x_axis, y_axis):
        self.x_axis = x_axis
        self.y_axis = y_axis

    def build(self):
        bar = Bar()
        bar.add_xaxis(self.x_axis)
        bar.add_yaxis(..., self.y_axis)
        return bar.render_embed()


if __name__ == '__main__':
    x_axis = ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"]
    y_axis = [5, 20, 36, 10, 75, 90]
    builder = EchartsBuilder(x_axis, y_axis)
    charts_html_code = builder.build()
    print(charts_html_code)

# from pyecharts.charts import Bar
# from pyecharts import options as opts
#
# # V1 版本开始支持链式调用
# # 你所看到的格式其实是 `black` 格式化以后的效果
# # 可以执行 `pip install black` 下载使用
# bar = (
#     Bar()
#     .add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
#     .add_yaxis("商家A", [5, 20, 36, 10, 75, 90])
#     .set_global_opts(title_opts=opts.TitleOpts(title="主标题", subtitle="副标题"))
#     # 或者直接使用字典参数
#     # .set_global_opts(title_opts={"text": "主标题", "subtext": "副标题"})
# )
# bar.render()
#
# # 不习惯链式调用的开发者依旧可以单独调用方法
# bar = Bar()
# bar.add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
# bar.add_yaxis("商家A", [5, 20, 36, 10, 75, 90])
# bar.set_global_opts(title_opts=opts.TitleOpts(title="主标题", subtitle="副标题"))
# bar.render()
