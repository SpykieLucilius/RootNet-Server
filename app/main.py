from fastapi import FastAPI

from .database import Base, engine
from .routes import readings, modules

# create tables on startup (idempotent)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart Pot API", version="0.1.0")


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(readings.router)
app.include_router(modules.router)
