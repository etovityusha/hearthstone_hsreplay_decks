import uvicorn
from fastapi import FastAPI

from api.decks.routes import router as decks_router
from api.healthcheck.routes import router as healthcheck_router
from database import engine, Base

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(decks_router)
app.include_router(healthcheck_router)

if __name__ == "__main__":
    uvicorn.run("run:app", host='0.0.0.0', port=6100, reload=True)
