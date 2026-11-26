from fastapi import APIRouter, Depends, status

from app.dependencies import get_device_service
from app.models import DeviceCreate, DeviceResponse, DeviceSummaryResponse, StatusUpdate
from app.services.probe import simulate_device_probe
from app.services.device_service import DeviceService


router = APIRouter(prefix="/devices", tags=["devices"])


@router.post(
	"",
	response_model=DeviceResponse,
	status_code=status.HTTP_201_CREATED,
	responses={409: {"description": "A device with this ID already exists"}},
)
def register_device(
	device: DeviceCreate,
	service: DeviceService = Depends(get_device_service),
) -> DeviceResponse:
	return service.register(device)


@router.get("", response_model=list[DeviceResponse])
def list_devices(
	service: DeviceService = Depends(get_device_service),
) -> list[DeviceResponse]:
	return service.list()


@router.get("/summary", response_model=DeviceSummaryResponse)
def get_device_summary(
	service: DeviceService = Depends(get_device_service),
) -> DeviceSummaryResponse:
	return service.get_device_summary()


@router.get("/{device_id}/probe")
async def probe_device(
	device_id: str,
	service: DeviceService = Depends(get_device_service),
) -> dict[str, str | bool]:
	service.get_device(device_id)
	return await simulate_device_probe(device_id)


@router.get(
	"/{device_id}",
	response_model=DeviceResponse,
	responses={404: {"description": "Device not found"}},
)
def get_device(
	device_id: str,
	service: DeviceService = Depends(get_device_service),
) -> DeviceResponse:
	return service.get(device_id)


@router.patch(
	"/{device_id}/status",
	response_model=DeviceResponse,
	responses={404: {"description": "Device not found"}},
)
def update_device_status(
	device_id: str,
	status_update: StatusUpdate,
	service: DeviceService = Depends(get_device_service),
) -> DeviceResponse:
	return service.update_status(device_id, status_update)
