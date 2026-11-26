from copy import deepcopy

from app.models import AlertResponse, DeviceResponse, DeviceStatus, StatusUpdate


class InMemoryDeviceRepository:
	def __init__(self) -> None:
		self._devices: dict[str, DeviceResponse] = {}
		self._alerts: list[AlertResponse] = []

	def add_device(self, device: DeviceResponse) -> DeviceResponse:
		stored_device = deepcopy(device)
		self._devices[stored_device.device_id] = stored_device
		return deepcopy(stored_device)

	def list_devices(self) -> list[DeviceResponse]:
		return deepcopy(list(self._devices.values()))

	def get_device(self, device_id: str) -> DeviceResponse | None:
		device = self._devices.get(device_id)
		return deepcopy(device) if device is not None else None

	def update_status(
		self, device_id: str, status: DeviceStatus | StatusUpdate
	) -> DeviceResponse | None:
		device = self._devices.get(device_id)
		if device is None:
			return None

		status_value = status.status if isinstance(status, StatusUpdate) else StatusUpdate(status=status).status
		updated_device = deepcopy(device)
		updated_device.status = status_value
		self._devices[device_id] = updated_device
		return deepcopy(updated_device)

	def save_alert(self, alert: AlertResponse) -> AlertResponse:
		stored_alert = deepcopy(alert)
		self._alerts.append(stored_alert)
		return deepcopy(stored_alert)

	def list_alerts(self) -> list[AlertResponse]:
		return deepcopy(self._alerts)
