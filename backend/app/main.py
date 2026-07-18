from fastapi import FastAPI
from app.config import SETTINGS
from app.api.ws_live import router as websocket_router

app = FastAPI(
    title=SETTINGS["APP_NAME"],
    version=SETTINGS["VERSION"],
)

app.include_router(websocket_router)


@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "app": SETTINGS["APP_NAME"],
        "version": SETTINGS["VERSION"],
        "environment": SETTINGS["ENVIRONMENT"],
    }