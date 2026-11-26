import pytest

from app.models import DeviceCreate
from app.repositories.device_repository import InMemoryDeviceRepository
from app.services.device_service import (
    DeviceAlreadyExistsError,
    DeviceNotFoundError,
    DeviceService,
)


@pytest.fixture
def service_and_repository() -> tuple[DeviceService, InMemoryDeviceRepository]:
    repository = InMemoryDeviceRepository()
    return DeviceService(repository), repository


def make_device(device_id: str = "router-01", status: str = "online") -> DeviceCreate:
    return DeviceCreate(
        device_id=device_id,
        name="Main router",
        device_type="router",
        ip_address="192.168.1.10",
        status=status,
    )


def test_registration(service_and_repository) -> None:
    service, _ = service_and_repository

    device = service.register(make_device())

    assert device.device_id == "router-01"
    assert device.status == "online"
    assert service.get("router-01") == device
    assert service.list() == [device]


def test_duplicate_registration_raises_device_already_exists(service_and_repository) -> None:
    service, _ = service_and_repository
    service.register(make_device())

    with pytest.raises(DeviceAlreadyExistsError):
        service.register(make_device())


def test_get_missing_device_raises_device_not_found(service_and_repository) -> None:
    service, _ = service_and_repository

    with pytest.raises(DeviceNotFoundError):
        service.get("missing-device")


def test_updating_missing_device_raises_device_not_found(service_and_repository) -> None:
    service, _ = service_and_repository

    with pytest.raises(DeviceNotFoundError):
        service.update_status("missing-device", "offline")


def test_initial_offline_registration_does_not_create_alert(service_and_repository) -> None:
    service, repository = service_and_repository

    service.register(make_device(status="offline"))

    assert repository.list_alerts() == []


def test_online_to_offline_creates_one_alert(service_and_repository) -> None:
    service, repository = service_and_repository
    service.register(make_device())

    updated_device = service.update_status("router-01", "offline")

    alerts = repository.list_alerts()
    assert updated_device.status == "offline"
    assert len(alerts) == 1
    assert alerts[0].device_id == "router-01"
    assert "went offline" in alerts[0].message
    assert alerts[0].timestamp.utcoffset().total_seconds() == 0


def test_repeated_offline_update_does_not_create_another_alert(service_and_repository) -> None:
    service, repository = service_and_repository
    service.register(make_device())
    service.update_status("router-01", "offline")

    service.update_status("router-01", "offline")

    assert len(repository.list_alerts()) == 1
