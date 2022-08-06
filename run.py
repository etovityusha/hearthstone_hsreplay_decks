import uvicorn
from fastapi import FastAPI

from api.decks.routes import router as decks_router
from api.healthcheck.routes import router as healthcheck_router


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(decks_router)
    app.include_router(healthcheck_router)
    return app


if __name__ == "__main__":
    app = create_app()
    uvicorn.run("run:app", host='0.0.0.0', port=6100, reload=True)
