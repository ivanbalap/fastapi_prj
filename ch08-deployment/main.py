import fastapi
import uvicorn
from starlette.staticfiles import StaticFiles
from pathlib import Path
import json
from services import openweather_service, report_service
from models.location import Location
import asyncio
from api import weather_api
from views import home

api = fastapi.FastAPI()


def configure():
    configure_routing()
    configure_apikeys()
    configure_fake_data()


def configure_apikeys():
    file = Path("settings.json").absolute()
    if not file.exists():
        print("WARNING: {file} file not found")
        raise Exception("settings.json not found")

    with open("settings.json") as fin:
        settings = json.load(fin)
        openweather_service.api_key = settings.get("api_key")


def configure_routing():
    api.mount("/static", StaticFiles(directory="static"), name="static")
    api.include_router(home.router)
    api.include_router(weather_api.router)


def configure_fake_data():
    loc = Location(city="Portland", state="OR", country="US")
    asyncio.run(report_service.add_report("Misty sunrise today, beautiful!", loc))
    asyncio.run(report_service.add_report("Clouds over downtown", loc))


if __name__ == "__main__":
    configure()
    uvicorn.run(api, port=8000, host="127.0.0.1")
else:
    configure()
