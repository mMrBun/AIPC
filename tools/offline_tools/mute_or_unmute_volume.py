"""
This is a tool based on langchain BaseTool class,
where you can define the input parameters and the implementation logic for the tool.
Please describe the parameters and the purpose of the tool in as much detail as possible,
as this can help the model work better.
"""
import abc
import json
import os
import subprocess
from typing import Any, Type
from server.extras.packages import is_pycaw_available

if is_pycaw_available():
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
    from ctypes import cast, POINTER
    from comtypes import CLSCTX_ALL

from langchain.tools import BaseTool
from pydantic import BaseModel, Field

from configs.base_config import CURRENT_PLATFORM


class MuteVolumeInput(BaseModel):
    mute_type: str = Field(description="mute or unmute", examples=["mute", "unmute"], default="mute")


class MuteVolume(BaseTool, abc.ABC):
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
    name = "mute_volume"
    description = "mute or unmute the volume level of the audio"
    args_schema: Type[BaseModel] = MuteVolumeInput
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
        def mute_windows():
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            volume.SetMute(1, None)

        def unmute_windows():
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            volume.SetMute(0, None)

        def mute_macos():
            subprocess.run(["osascript", "-e", "set volume output muted true"])

        def unmute_macos():
            subprocess.run(["osascript", "-e", "set volume output muted false"])

        def mute_linux():
            subprocess.run(["amixer", "set", "Master", "mute"])

        def unmute_linux():
            subprocess.run(["amixer", "set", "Master", "unmute"])

        try:
            current_os = CURRENT_PLATFORM
            mute_type = kwargs.get("mute_type")
            if current_os == "Windows":
                if mute_type == "mute":
                    mute_windows()
                elif mute_type == "unmute":
                    unmute_windows()
            elif current_os == "macOS":
                if mute_type == "mute":
                    mute_macos()
                elif mute_type == "unmute":
                    unmute_macos()
            elif current_os == "Linux":
                if mute_type == "mute":
                    mute_linux()
                elif mute_type == "unmute":
                    unmute_linux()
            else:
                return json.dumps({"code": 500, "msg": "Unsupported OS", "data": {}})
            return json.dumps({"code": 200, "msg": "success", "data": {"mute_type": mute_type, "os": current_os}})
        except Exception as e:
            return json.dumps({"code": 500, "msg": str(e)[-40:], "data": {}})
