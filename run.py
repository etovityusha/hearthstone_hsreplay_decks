import uvicorn
from fastapi import FastAPI

from database import engine, Base
from api.decks.routes import router as decks_router

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(decks_router)


if __name__ == "__main__":
    uvicorn.run("run:app", host='0.0.0.0', port=5000, reload=True)
