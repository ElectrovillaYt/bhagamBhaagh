from fastapi import APIRouter, status
from app.core.config import settings
import httpx
from app.core.exceptions import NotFoundError

router = APIRouter(
    prefix="/api/v1/map",
    tags=["map"]
)


@router.get(
    "/tiles",
    status_code=status.HTTP_200_OK
)
async def getTiles():
    URL = f'https://api.maptiler.com/maps/openstreetmap/style.json?key={settings.MAP_TILER_KEY}'
    async with httpx.AsyncClient() as client:
        response = await client.get(URL)
        if response.status_code != 200:
            return NotFoundError(f'Tiler API Request Failed! Status:{response.status_code}')
        return response.json()