"""
This is a tool based on langchain BaseTool class,
where you can define the input parameters and the implementation logic for the tool.
Please describe the parameters and the purpose of the tool in as much detail as possible,
as this can help the model work better.
"""
import abc
import json
from typing import Type
from langchain.tools import BaseTool
from pydantic import BaseModel, Field


class WeatherInput(BaseModel):
    location: str = Field(description="Location, city, state.", examples=['beijing', 'Miami'], default="beijing")
    unit: str = Field(description="Types of temperature", examples=['celsius', 'fahrenheit'], default="fahrenheit")


class Weather(BaseTool, abc.ABC):
    """
    🤗name: The name of the tool may require specific prefix words like "get_" in the inference client of some models.
    Please adjust the naming format here accordingly based on the differences between models.
    🤗description: Please provide as clear a description as possible of the tool,
    detailing what it is used for, what problem it solves, and the scenarios in which it is used.
    This can increase the accuracy of model selection for the right tool.
    🤗args_schema: For the tool input parameters, if possible, please provide a description, examples,
     and default values for each parameter.
    """
    name = "get_current_weather"
    description = "Get the current weather in a given location"
    args_schema: Type[BaseModel] = WeatherInput

    def __init__(self):
        super().__init__()

    def _run(self, location: str, unit: str) -> str:
        """
        Write down the implementation logic for the tool here.
        """
        if "tokyo" in location.lower():
            return json.dumps({"location": "Tokyo", "temperature": "10", "unit": unit})
        elif "san francisco" in location.lower():
            return json.dumps({"location": "San Francisco", "temperature": "72", "unit": unit})
        elif "paris" in location.lower():
            return json.dumps({"location": "Paris", "temperature": "22", "unit": unit})
        else:
            return json.dumps({"location": location, "temperature": "unknown"})
