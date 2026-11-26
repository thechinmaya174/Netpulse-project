from fastapi import APIRouter, Depends

from app.dependencies import get_device_repository
from app.models import AlertResponse
from app.repositories.device_repository import InMemoryDeviceRepository


router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.get("", response_model=list[AlertResponse])
def list_alerts(
	repository: InMemoryDeviceRepository = Depends(get_device_repository),
) -> list[AlertResponse]:
	return repository.list_alerts()