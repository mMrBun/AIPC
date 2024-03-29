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
from typing import Any
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from langchain.tools import BaseTool
from pydantic import BaseModel, Field


class SetVolumeInput(BaseModel):
    volume_level: float = Field(description="volume level, range: 0.0 - 1.0", examples=[0.1, 0.5, 1], default="0.02")


class SetVolume(BaseTool, abc.ABC):
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
    name = "set_volume"
    description = "set the volume level of the audio"
    enabled = True

    def __init__(self):
        super().__init__()

    async def _arun(
            self,
            *args: Any,
            **kwargs: Any,
    ) -> Any:
        def get_os():
            platform = os.name
            if platform == 'nt':
                return 'Windows'
            elif platform == 'posix':
                from sys import platform as _platform
                if _platform == 'darwin':
                    return 'macOS'
                elif _platform == 'linux' or _platform == 'linux2':  # Linux
                    return 'Linux'
            return 'Unknown'

        def set_volume_windows(volume_level: float):
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            volume.SetMasterVolumeLevelScalar(volume_level, None)

        def set_volume_macos(volume_level):
            subprocess.run(["osascript", "-e", f"set volume output volume {volume_level}"])

        def set_volume_linux(volume_level):
            subprocess.run(["amixer", "set", "Master", f"{volume_level}%"])

        try:
            current_os = get_os()
            volume_level = kwargs.get("volume_level")
            if current_os == "Windows":
                set_volume_windows(volume_level)
            elif current_os == "macOS":
                set_volume_macos(volume_level)
            elif current_os == "Linux":
                set_volume_linux(volume_level)
            else:
                return json.dumps({"code": 500, "msg": "Unsupported OS", "data": {}})
            return json.dumps({"code": 200, "msg": "success", "data": {"volume_level": volume_level, "os": current_os}})
        except Exception as e:
            return json.dumps({"code": 500, "msg": str(e)[-40:], "data": {}})
