import os
from tortoise import Tortoise

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgres://user:password@localhost:5432/water_quality"
).replace("postgresql+asyncpg://", "postgres://")

if os.getenv("TESTING") == "1":
    DATABASE_URL = "sqlite://:memory:"

TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "models": {
            "models": ["src.repository.models"],
            "default_connection": "default",
        }
    },
}


async def init_db():
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas(safe=True)


async def close_db():
    await Tortoise.close_connections()
