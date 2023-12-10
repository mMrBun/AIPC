import re

string = """
var option_5533c880c6504289bf2be76d8c6b2e89 = {
    "animation": true,
    "animationThreshold": 2000,
    "animationDuration": 1000,
    "animationEasing": "cubicOut",
    "animationDelay": 0,
    "animationDurationUpdate": 300,
    "animationEasingUpdate": "cubicOut",
    "animationDelayUpdate": 0,
    "aria": {
        "enabled": false
    },
    "color": [
        "#5470c6",
        "#91cc75",
        "#fac858",
        "#ee6666",
        "#73c0de",
        "#3ba272",
        "#fc8452",
        "#9a60b4",
        "#ea7ccc"
    ],
    "series": [
        {
            "type": "line",
            "name": "\u6d88\u8d39\u91d1\u989d",
            "connectNulls": false,
            "xAxisIndex": 0,
            "symbolSize": 4,
            "showSymbol": true,
            "smooth": false,
            "clip": true,
            "step": false,
            "data": [
                [
                    "1\u6708",
                    569.23
                ],
                [
                    "2\u6708",
                    460.74
                ],
                [
                    "3\u6708",
                    541.36
                ],
                [
                    "4\u6708",
                    682.78
                ],
                [
                    "5\u6708",
                    159.35
                ],
                [
                    "6\u6708",
                    357.12
                ],
                [
                    "7\u6708",
                    852.46
                ],
                [
                    "8\u6708",
                    741.32
                ],
                [
                    "9\u6708",
                    369.54
                ],
                [
                    "10\u6708",
                    523.98
                ],
                [
                    "11\u6708",
                    412.69
                ],
                [
                    "12\u6708",
                    785.95
                ]
            ],
            "hoverAnimation": true,
            "label": {
                "show": true,
                "margin": 8
            },
            "logBase": 10,
            "seriesLayoutBy": "column",
            "lineStyle": {
                "show": true,
                "width": 1,
                "opacity": 1,
                "curveness": 0,
                "type": "solid"
            },
            "areaStyle": {
                "opacity": 0
            },
            "zlevel": 0,
            "z": 0
        }
    ],
    "legend": [
        {
            "data": [
                "\u6d88\u8d39\u91d1\u989d"
            ],
            "selected": {}
        }
    ],
    "tooltip": {
        "show": true,
        "trigger": "item",
        "triggerOn": "mousemove|click",
        "axisPointer": {
            "type": "line"
        },
        "showContent": true,
        "alwaysShowContent": false,
        "showDelay": 0,
        "hideDelay": 100,
        "enterable": false,
        "confine": false,
        "appendToBody": false,
        "transitionDuration": 0.4,
        "textStyle": {
            "fontSize": 14
        },
        "borderWidth": 0,
        "padding": 5,
        "order": "seriesAsc"
    },
    "xAxis": [
        {
            "show": true,
            "scale": false,
            "nameLocation": "end",
            "nameGap": 15,
            "gridIndex": 0,
            "inverse": false,
            "offset": 0,
            "splitNumber": 5,
            "minInterval": 0,
            "splitLine": {
                "show": true,
                "lineStyle": {
                    "show": true,
                    "width": 1,
                    "opacity": 1,
                    "curveness": 0,
                    "type": "solid"
                }
            },
            "data": [
                "1\u6708",
                "2\u6708",
                "3\u6708",
                "4\u6708",
                "5\u6708",
                "6\u6708",
                "7\u6708",
                "8\u6708",
                "9\u6708",
                "10\u6708",
                "11\u6708",
                "12\u6708"
            ]
        }
    ],
    "yAxis": [
        {
            "show": true,
            "scale": false,
            "nameLocation": "end",
            "nameGap": 15,
            "gridIndex": 0,
            "inverse": false,
            "offset": 0,
            "splitNumber": 5,
            "minInterval": 0,
            "splitLine": {
                "show": true,
                "lineStyle": {
                    "show": true,
                    "width": 1,
                    "opacity": 1,
                    "curveness": 0,
                    "type": "solid"
                }
            }
        }
    ]
};
"""

# 构建正则表达式以匹配变量名和它的值
# 这里假设值是一个对象，由大括号包裹
pattern = r'var option_([a-f0-9]{32}) = \{(.*?)\};'

# 使用正则表达式搜索字符串内容
matches = re.findall(pattern, string, re.DOTALL)

# 检查是否找到匹配，并获取值
if matches:
    for match in matches:
        uid, value = match
        print(f"找到变量: option_{uid}，值为: {{{value}}}")
else:
    print("没有找到匹配的JS变量。")
