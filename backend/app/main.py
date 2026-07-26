from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import SETTINGS
from app.api.ws_live import router as websocket_router
from app.api.routes_auth import router as auth_router
from app.api.routes_tasks import router as tasks_router

app = FastAPI(
    title=SETTINGS["APP_NAME"],
    version=SETTINGS["VERSION"],
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:5175"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(websocket_router)
app.include_router(auth_router)
app.include_router(tasks_router)

@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "app": SETTINGS["APP_NAME"],
        "version": SETTINGS["VERSION"],
        "environment": SETTINGS["ENVIRONMENT"],
    }