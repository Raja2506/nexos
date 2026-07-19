import os
from pathlib import Path
from typing import Dict
from dotenv import load_dotenv


def load_environment(env_path: Path | None = None) -> Dict[str, str]:
    resolved_path = env_path or Path(__file__).resolve().parent.parent / ".env"

    if resolved_path.exists():
        load_dotenv(resolved_path, override=True)

    return {
        "APP_NAME": os.getenv("APP_NAME", "NexOS"),
        "VERSION": os.getenv("VERSION", "0.1.0"),
        "ENVIRONMENT": os.getenv("ENVIRONMENT", "development"),
        "PORT": os.getenv("PORT", "8000"),
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY", ""),
        "ANTHROPIC_API_KEY": os.getenv("ANTHROPIC_API_KEY", ""),
        "DATABASE_URL": os.getenv("DATABASE_URL", ""),
        "REDIS_URL": os.getenv("REDIS_URL", "redis://localhost:6379/0"),
        "CHROMA_PERSIST_DIR": os.getenv("CHROMA_PERSIST_DIR", "./chroma_data"),
        "GEMINI_API_KEY": os.getenv("GEMINI_API_KEY", ""),
        "JWT_SECRET": os.getenv("JWT_SECRET", "dev-secret-change-me"),
    }


SETTINGS = load_environment()
