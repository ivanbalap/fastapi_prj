from typing import Optional, Tuple

# import requests
import httpx
from infrastructure import weather_cache
from httpx import Response
from models.validation_error import ValidationError

api_key: Optional[str] = None


async def get_report_async(
    city: str, state: Optional[str], country: str, units: str
) -> dict:
    # url = f"https://api.openweathermap.org/data/2.5/weather?q={city name},{state code},{country code}&appid={API key}"
    city, state, country, units = validate_units(city, state, country, units)
    
    if forecast := weather_cache.get_weather(city, state, country, units):
        return forecast

    if state:
        q = f"{city},{state},{country}"
    else:
        q = f"{city},{country}"
    # key = 123
    url = f"https://api.openweathermap.org/data/2.5/weather?q={q}&appid={api_key}&units={units}"
    # print(url)

    async with httpx.AsyncClient() as client:
        # resp = await client.get(url)
        # resp.raise_for_status()
        resp: Response = await client.get(url)
        if resp.status_code != 200:
            raise ValidationError(resp.text, resp.status_code)

    data = resp.json()
    forecast = data["main"]

    weather_cache.set_weather(city, state, country, units, forecast)

    return forecast


def validate_units(
    city: str, state: Optional[str], country: Optional[str], units: str
) -> Tuple[str, Optional[str], str, str]:
    city = city.lower().strip()
    if not country:
        country = "us"
    else:
        country = country.lower().strip()

    if len(country) != 2:
        error = f"Invalid country: {country}. It must be a two letter abbreviation such as US or GB"
        raise ValidationError(status_code=400, error_msg=error)

    if state:
        state = state.strip().lower()

    if state and len(state) != 2:
        error = f"Invalid state: {state}. It must be a two letter abbreviation such as CA or KS"
        raise ValidationError(status_code=400, error_msg=error)

    if units:
        units = units.lower().strip()

    valid_units = {"standard", "metric", "imperial"}
    if units not in valid_units:
        error = f"Invalid units '{units}', it must be one of {valid_units}"
        raise ValidationError(status_code=400, error_msg=error)

    return city, state, country, units
