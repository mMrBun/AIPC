"""
This is a tool based on langchain BaseTool class,
where you can define the input parameters and the implementation logic for the tool.
Please describe the parameters and the purpose of the tool in as much detail as possible,
as this can help the model work better.
"""
import abc
import json
import os
from typing import Any
from langchain.tools import BaseTool
from pydantic import BaseModel, Field

from configs.base_config import CURRENT_PLATFORM


class SetBrightnessInput(BaseModel):
    theme_type: int = Field(description="type of theme: dark or light", examples=['dark', 'light'])


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
    name = "set_theme"
    description = "set global theme of the PC"
    enabled = True

    def __init__(self):
        super().__init__()

    async def _arun(
            self,
            *args: Any,
            **kwargs: Any,
    ) -> Any:

        DARK_SYSTEM = "reg.exe add HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize /v SystemUsesLightTheme /t REG_DWORD /d 0 /f"
        DARK_APPS = "reg.exe add HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize /v AppsUseLightTheme /t REG_DWORD /d 0 /f"
        LIGHT_SYSTEM = "reg.exe add HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize /v SystemUsesLightTheme /t REG_DWORD /d 1 /f"
        LIGHT_APPS = "reg.exe add HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize /v AppsUseLightTheme /t REG_DWORD /d 1 /f"

        ver = int(os.popen("ver").read()[28:33]) >= 18362

        def dark():
            os.system(DARK_SYSTEM)
            if ver:
                os.system(DARK_APPS)
            return 0

        def light():
            os.system(LIGHT_SYSTEM)
            if ver:
                os.system(LIGHT_APPS)
            return 0

        try:
            current_os = CURRENT_PLATFORM
            theme_type = kwargs.get("theme_type")
            if theme_type not in ['dark', 'light']:
                return json.dumps({"code": 500, "msg": "Unsupported theme type", "data": {}})
            if current_os == "Windows":
                if theme_type == 'dark':
                    dark()
                elif theme_type == 'light':
                    light()
                else:
                    return json.dumps({"code": 500, "msg": "Unsupported theme type", "data": {}})
            elif current_os == "macOS":
                return json.dumps({"code": 500, "msg": "Unsupported OS", "data": {}})
            elif current_os == "Linux":
                return json.dumps({"code": 500, "msg": "Unsupported OS", "data": {}})
            else:
                return json.dumps({"code": 500, "msg": "Unsupported OS", "data": {}})
            return json.dumps({"code": 200, "msg": "success", "data": {"theme_type": theme_type, "os": current_os}})
        except Exception as e:
            return json.dumps({"code": 500, "msg": str(e)[-40:], "data": {}})