tools = [
    {
        "name": "number_of_product_sales",
        "description": "查询各类产品的销售数量",
        "parameters": {}
    },
    {
        "name": "monthly_sales_revenue",
        "description": "每月销售额",
        "parameters": {}
    },
    {
        "name": "distribution_of_customer_age_groups",
        "description": "客户年龄分布",
        "parameters": {}
    }
]
tools_system_info = {"role": "system",
                     "content": "Answer the following questions as best as you can. You have access to the following tools:",
                     "tools": tools}
