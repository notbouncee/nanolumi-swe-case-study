from fastapi import APIRouter
from src.api.routes import device_routes, measurement_routes

api_router = APIRouter(prefix="/api")

api_router.include_router(device_routes.router, tags=["devices"])
api_router.include_router(measurement_routes.router, tags=["measurements"])
