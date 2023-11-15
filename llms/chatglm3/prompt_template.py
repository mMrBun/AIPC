
def create_prompt(data):
    template = f"""
    Please draw a line chart based on the following data format.
    ```
    {data}
    ```
    """
    return template


# f"""
#             你的任务是从饼图、柱状图、折线图、中选择一个根据data中的数据生成echars格式的javascript代码
#             这里有几点规则
#             1、只生成option部分的代码
#             2、禁止使用示例代码中数据
#             3、不要出现类似//...的省略，请补全
#             下面是三种图表的例子，仅作为格式参考
#             ```Bar chart
#             var option = {{
#                   title: {{
#                     text: "ECharts"
#                   }},
#                   tooltip: {{}},
#                   legend: {{
#                     data: ["销量"]
#                   }},
#                   xAxis: {{
#                     data: ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"]
#                   }},
#                   yAxis: {{}},
#                   series: [{{
#                     name: "销量",
#                     type: "bar",
#                     data: [5, 20, 36, 10, 10, 20]
#                   }}]
#                 }};
#
#             myChart.setOption(option);
#             ```
#             ```Line chart
#             var option = {{
#               xAxis: {{
#                 type: 'category',
#                 data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
#               }},
#               yAxis: {{
#                 type: 'value'
#               }},
#               series: [
#                 {{
#                   data: [150, 230, 224, 218, 135, 147, 260],
#                   type: 'line'
#                 }}
#               ]
#             }};
#
#             myChart.setOption(option);
#             ```
#             ```Pie chart
#             var option = {{
#               title: {{
#                 text: 'Referer of a Website',
#                 subtext: 'Fake Data',
#                 left: 'center'
#               }},
#               tooltip: {{
#                 trigger: 'item'
#               }},
#               legend: {{
#                 orient: 'vertical',
#                 left: 'left'
#               }},
#               series: [
#                 {{
#                   name: 'Access From',
#                   type: 'pie',
#                   radius: '50%',
#                   data: [
#                     {{ value: 1048, name: 'Search Engine' }},
#                     {{ value: 735, name: 'Direct' }},
#                     {{ value: 580, name: 'Email' }},
#                     {{ value: 484, name: 'Union Ads' }},
#                     {{ value: 300, name: 'Video Ads' }}
#                   ],
#                   emphasis: {{
#                     itemStyle: {{
#                       shadowBlur: 10,
#                       shadowOffsetX: 0,
#                       shadowColor: 'rgba(0, 0, 0, 0.5)'
#                     }}
#                   }}
#                 }}
#               ]
#             }};
#             ```
#
#             ```data
#             {data}
#             ```
#             """