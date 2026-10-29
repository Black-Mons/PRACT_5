import asyncio
import aiohttp
import json
import time
from datetime import datetime
MAKES_API_URL = "https://vpic.nhtsa.dot.gov/api/vehicles/getallmakes?format=json"
MODELS_API_URL = "https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMake/honda?format=json"
async def fetch_data(url, session):
    try:
        async with session.get(url, timeout=5) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                print(f"Ошибка {response.status} при запросе {url}")
    except asyncio.TimeoutError:
        print(f"Таймаут при запросе {url}")
    except Exception as e:
        print(f"Ошибка {e} при запросе {url}")
    return None
async def get_car_info():
    async with aiohttp.ClientSession() as session:
        makes_task = fetch_data(MAKES_API_URL, session)
        models_task = fetch_data(MODELS_API_URL, session)
        makes_data, models_data = await asyncio.gather(makes_task, models_task)
        return {
            "makes_sample": (makes_data or {}).get("Results", [])[:5],
            "models_sample": (models_data or {}).get("Results", [])[:5],
            "timestamp": datetime.now().isoformat()
        }
def save_data(data, filename="car_data.json"):
    with open(filename, "a") as file:
        file.write(json.dumps(data)+"\n")
async def main():
    while True:
        data = await get_car_info()
        if data:
            save_data(data)
            print(f"Данные сохранены: {data}")
        await asyncio.sleep(600)
if __name__ == "__main__":
    asyncio.run(main())
