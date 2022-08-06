from fastapi.routing import APIRouter

from api import decks, healthcheck

api_router = APIRouter()
api_router.include_router(decks.router)
api_router.include_router(healthcheck.router)
