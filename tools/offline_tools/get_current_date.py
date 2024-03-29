"""
This is a tool based on langchain BaseTool class,
where you can define the input parameters and the implementation logic for the tool.
Please describe the parameters and the purpose of the tool in as much detail as possible,
as this can help the model work better.
"""
import abc
import json
from typing import Any

from langchain.tools import BaseTool


class GetCurrentDate(BaseTool, abc.ABC):
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
    name = "get_current_date"
    description = "Get the current date"
    enabled = True

    def __init__(self):
        super().__init__()

    def _run(self) -> str:
        """
        Please provide a detailed description of the implementation logic of the tool.
        This can help the model understand the tool better and use it more accurately.
        """
        import datetime
        return json.dumps({"time": datetime.datetime.now().strftime("%Y-%m-%d")})

    async def _arun(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        import datetime
        return json.dumps({"time": datetime.datetime.now().strftime("%Y-%m-%d")})
