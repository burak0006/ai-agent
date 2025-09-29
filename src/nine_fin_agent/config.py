"""loading environment variables"""
from functools import lru_cache
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseModel):
    openai_api_key: str
    model: str
    redis_url: str
    qdrant_host: str
    qdrant_port: str
    qdrant_collection: str


@lru_cache()
def get_settings() -> Settings:
    return Settings(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        model=os.getenv("OPENAI_MODEL"),
        redis_url=os.getenv("REDIS_URL"),
        qdrant_host=os.getenv("QDRANT_HOST"),
        qdrant_port=os.getenv("QDRANT_PORT"),
        qdrant_collection=os.getenv("QDRANT_COLLECTION"),
    )

settings = get_settings()