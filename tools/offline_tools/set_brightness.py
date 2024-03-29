"""
This is a tool based on langchain BaseTool class,
where you can define the input parameters and the implementation logic for the tool.
Please describe the parameters and the purpose of the tool in as much detail as possible,
as this can help the model work better.
"""
import abc
import json
from server.extras.packages import is_screen_brightness_control_available

if is_screen_brightness_control_available():
    import screen_brightness_control as sbc
from typing import Any, Type
from langchain.tools import BaseTool
from pydantic import BaseModel, Field

from configs.base_config import CURRENT_PLATFORM


class SetBrightnessInput(BaseModel):
    brightness_level: int = Field(description="brightness level, range: 0 - 100", examples=[0, 20, 56, 100], default=50)


class SetBrightness(BaseTool, abc.ABC):
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
    name = "set_brightness"
    description = "set the brightness level of the screen"
    args_schema: Type[BaseModel] = SetBrightnessInput
    enabled = True

    def __init__(self):
        super().__init__()

    def _run(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        pass

    async def _arun(
            self,
            *args: Any,
            **kwargs: Any,
    ) -> Any:

        def set_brightness_windows(brightness_level: int):
            sbc.set_brightness(brightness_level)

        try:
            current_os = CURRENT_PLATFORM
            brightness_level = kwargs.get("brightness_level")
            if current_os == "Windows":
                set_brightness_windows(brightness_level)
            elif current_os == "macOS":
                return json.dumps({"code": 500, "msg": "Unsupported OS", "data": {}})
            elif current_os == "Linux":
                return json.dumps({"code": 500, "msg": "Unsupported OS", "data": {}})
            else:
                return json.dumps({"code": 500, "msg": "Unsupported OS", "data": {}})
            return json.dumps(
                {"code": 200, "msg": "success", "data": {"volume_level": brightness_level, "os": current_os}})
        except Exception as e:
            return json.dumps({"code": 500, "msg": str(e)[-40:], "data": {}})
