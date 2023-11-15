
def create_prompt(data):
    template = f"""
    Please draw a line chart based on the following data format.
    ```
    {data}
    ```
    """
    return template
