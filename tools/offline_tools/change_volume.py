"""
This is a tool based on langchain BaseTool class,
where you can define the input parameters and the implementation logic for the tool.
Please describe the parameters and the purpose of the tool in as much detail as possible,
as this can help the model work better.
"""
import abc
import json
from typing import Any
from server.extras.packages import is_pycaw_available

if is_pycaw_available():
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
    from ctypes import cast, POINTER
    from comtypes import CLSCTX_ALL

from langchain.tools import BaseTool
from pydantic import BaseModel, Field

from configs.base_config import CURRENT_PLATFORM


class ChangeVolumeInput(BaseModel):
    type: float = Field(description="turn up or turn down volume", examples=["up", "down"], default="up")


class ChangeVolume(BaseTool, abc.ABC):
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
    name = "change_volume"
    description = "turn up or turn down the volume level of the audio"
    enabled = True

    def __init__(self):
        super().__init__()

    async def _arun(
            self,
            *args: Any,
            **kwargs: Any,
    ) -> Any:
        volume_bias = 0.05

        def change_windows(type: str):
            if type not in ["up", "down"]:
                raise ValueError("type must be 'up' or 'down'")
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            if type == "up":
                current_volume = volume.GetMasterVolumeLevelScalar()
                if current_volume + volume_bias > 1:
                    volume.SetMasterVolumeLevelScalar(1, None)
                else:
                    volume.SetMasterVolumeLevelScalar(current_volume + volume_bias, None)
            else:
                current_volume = volume.GetMasterVolumeLevelScalar()
                if current_volume - volume_bias < 0:
                    volume.SetMasterVolumeLevelScalar(0, None)
                else:
                    volume.SetMasterVolumeLevelScalar(current_volume - volume_bias, None)
        try:
            current_os = CURRENT_PLATFORM
            type = kwargs.get("type")
            if current_os == "Windows":
                change_windows(type)
            elif current_os == "macOS":
                return json.dumps({"code": 500, "msg": "Unsupported OS", "data": {}})
            elif current_os == "Linux":
                return json.dumps({"code": 500, "msg": "Unsupported OS", "data": {}})
            else:
                return json.dumps({"code": 500, "msg": "Unsupported OS", "data": {}})
            return json.dumps({"code": 200, "msg": "success", "data": {"mute_type": type, "os": current_os}})
        except Exception as e:
            return json.dumps({"code": 500, "msg": str(e)[-40:], "data": {}})
