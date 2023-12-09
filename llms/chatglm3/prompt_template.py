
def create_prompt(data):
    template = f"""
    Please draw a line chart based on the following data format.
    ```
    {data}
    ```
    """
    return template


def create_system_prompt(tools):
    system_prompt = {"role": "system",
                     "content": "Answer the following questions as best as you can. You have access to the following core:",
                     "core": tools}

    return system_prompt
