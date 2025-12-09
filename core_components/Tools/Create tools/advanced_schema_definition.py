# 使用 Pydantic 模型或 JSON Schema 定义复杂输入：
from pydantic import BaseModel, Field
from typing import Literal
from langchain.tools import tool


class WeatherInput(BaseModel):
    """Input for weather queries."""
    location: str = Field(description="City name or coordinates")
    units: Literal["celsius", "fahrenheit"] = Field(
        default = "celsius",
        description = "Temperature units preference"
    )
    include_forecast: bool = Field(
        default = False,
        description="Include 5-day forecast"
    )

weather_schema = {
    "type": "object",
    "properties": {
        "location": {"type": "string"},
        "units": {"type": "string"},
        "include_forecast": {"type": "boolean"}
    },
    "required": ["location", "units", "include_forecast"]
}

@tool(args_schema = WeatherInput) # or use args_schema = weather_schema
def get_weather(location: str, units: str = "celsius", include_forecast: bool = False) -> str:
    """Get current weather and optional forecast."""
    temp = 22 if units == "celsius" else 72
    result = f"Current weather in {location}: {temp} degrees {units[0].upper()}"
    if include_forecast:
        result += "\nNext 5 days : Sunny"
    return result



