from fastapi import Depends, Request

from app.repositories.device_repository import InMemoryDeviceRepository
from app.services.device_service import DeviceService


def get_device_repository(request: Request) -> InMemoryDeviceRepository:
	return request.app.state.device_repository


def get_device_service(
	repository: InMemoryDeviceRepository = Depends(get_device_repository),
) -> DeviceService:
	return DeviceService(repository)