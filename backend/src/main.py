from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# pyrefly: ignore [missing-import]
from src.api.router import api_router
from src.client.db import TORTOISE_ORM
from src.service.device_service import sync_devices
from tortoise import Tortoise
from contextlib import asynccontextmanager
import logging
import os

logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("LIFESPAN STARTED")
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas(safe=True)
    if os.getenv("TESTING") != "1":
        await sync_devices()
    yield
    print("LIFESPAN ENDED")
    await Tortoise.close_connections()


app = FastAPI(title="Water Quality API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
