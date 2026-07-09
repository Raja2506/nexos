from fastapi import FastAPI

from app.config import SETTINGS

app = FastAPI(
    title=SETTINGS["APP_NAME"],
    version=SETTINGS["VERSION"],
)


@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "app": SETTINGS["APP_NAME"],
        "version": SETTINGS["VERSION"],
        "environment": SETTINGS["ENVIRONMENT"],
    }