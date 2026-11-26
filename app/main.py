from fastapi import FastAPI

from app.repositories.device_repository import InMemoryDeviceRepository
from app.routes.alerts import router as alerts_router
from app.routes.devices import router as devices_router
from app.routes.health import router as health_router


app = FastAPI(title="Device API")
app.state.device_repository = InMemoryDeviceRepository()
app.include_router(devices_router)
app.include_router(alerts_router)
app.include_router(health_router)
