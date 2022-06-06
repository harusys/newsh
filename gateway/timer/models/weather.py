from pydantic import BaseModel


class Weather(BaseModel):
    WeatherDescription: str
    Temperature: float
    MaxTemperature: float
    MinTemperature: float
