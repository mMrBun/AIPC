"""
This is a tool based on langchain BaseTool class,
where you can define the input parameters and the implementation logic for the tool.
Please describe the parameters and the purpose of the tool in as much detail as possible,
as this can help the model work better.
"""
import abc
import json
from typing import Type, Any
from langchain.tools import BaseTool
from pydantic import BaseModel, Field


class AnnualBillInput(BaseModel):
    year: str = Field(description="Year number", examples=[2023, 2024])


class AnnualBill(BaseTool, abc.ABC):
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
    name = "get_annual_bill"
    description = "Get the annual bill for a given year"
    args_schema: Type[BaseModel] = AnnualBillInput
    enabled = False

    def __init__(self):
        super().__init__()

    def _run(self, year: int) -> str:
        """
        Write down the implementation logic for the tool here.
        """

        bill = {
            "year": year,
            "bill": [
                {
                    "month": 1,
                    "cost": 100,
                },
                {
                    "month": 2,
                    "cost": 120,
                },
                {
                    "month": 3,
                    "cost": 90,
                },
                {
                    "month": 4,
                    "cost": 110,
                },
                {
                    "month": 5,
                    "cost": 130,
                },
                {
                    "month": 6,
                    "cost": 150,
                },
                {
                    "month": 7,
                    "cost": 140,
                },
                {
                    "month": 8,
                    "cost": 160,
                },
                {
                    "month": 9,
                    "cost": 170,
                },
                {
                    "month": 10,
                    "cost": 180,
                },
                {
                    "month": 11,
                    "cost": 190,
                },
                {
                    "month": 12,
                    "cost": 200,
                },
            ]
        }
        return json.dumps(bill)

    async def _arun(
            self,
            *args: Any,
            **kwargs: Any,
    ) -> Any:
        """
        Write down the implementation logic for the tool here.
        """
        bill = {
            "year": kwargs.get("year"),
            "bill": [
                {
                    "month": 1,
                    "cost": 100,
                },
                {
                    "month": 2,
                    "cost": 120,
                },
                {
                    "month": 3,
                    "cost": 90,
                },
                {
                    "month": 4,
                    "cost": 110,
                },
                {
                    "month": 5,
                    "cost": 130,
                },
                {
                    "month": 6,
                    "cost": 150,
                },
                {
                    "month": 7,
                    "cost": 140,
                },
                {
                    "month": 8,
                    "cost": 160,
                },
                {
                    "month": 9,
                    "cost": 170,
                },
                {
                    "month": 10,
                    "cost": 180,
                },
                {
                    "month": 11,
                    "cost": 190,
                },
                {
                    "month": 12,
                    "cost": 200,
                },
            ]
        }
        return json.dumps(bill)
