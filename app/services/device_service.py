from app.events import create_offline_alert
from app.models import (
	DeviceCreate,
	DeviceResponse,
	DeviceStatus,
	DeviceSummaryResponse,
	DeviceType,
	StatusUpdate,
)
from app.repositories.contracts import DeviceRepository


class DeviceAlreadyExistsError(Exception):
	pass


class DeviceNotFoundError(Exception):
	pass


class DeviceService:
	def __init__(self, repository: DeviceRepository) -> None:
		self._repository = repository

	def register(self, device: DeviceCreate) -> DeviceResponse:
		if self._repository.get_device(device.device_id) is not None:
			raise DeviceAlreadyExistsError(f"Device '{device.device_id}' already exists")

		response = DeviceResponse(
			device_id=device.device_id,
			name=device.name,
			device_type=device.device_type,
			ip_address=device.ip_address,
			status=device.status,
		)
		return self._repository.add_device(response)

	def list(self) -> list[DeviceResponse]:
		return self._repository.list_devices()

	def get_device_summary(self) -> DeviceSummaryResponse:
		devices = self._repository.list_devices()
		status_counts: dict[DeviceStatus, int] = {"online": 0, "offline": 0}
		device_types: set[DeviceType] = set()

		for device in devices:
			status_counts[device.status] += 1
			device_types.add(device.device_type)

		return DeviceSummaryResponse(
			total_devices=len(devices),
			online_count=status_counts["online"],
			offline_count=status_counts["offline"],
			device_types=sorted(device_types),
		)

	def get_device(self, device_id: str) -> DeviceResponse:
		device = self._repository.get_device(device_id)
		if device is None:
			raise DeviceNotFoundError(f"Device '{device_id}' was not found")
		return device

	def get(self, device_id: str) -> DeviceResponse:
		return self.get_device(device_id)

	def update_status(
		self, device_id: str, status_update: StatusUpdate | DeviceStatus
	) -> DeviceResponse:
		device = self.get(device_id)
		status = (
			status_update.status
			if isinstance(status_update, StatusUpdate)
			else StatusUpdate(status=status_update).status
		)
		updated_device = self._repository.update_status(device_id, status)
		if updated_device is None:
			raise DeviceNotFoundError(f"Device '{device_id}' was not found")

		if device.status == "online" and status == "offline":
			create_offline_alert(self._repository, device_id)

		return updated_device
