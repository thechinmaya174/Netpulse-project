import asyncio

from app.services.probe import simulate_device_probe


def test_simulate_device_probe_returns_fixed_result() -> None:
	result = asyncio.run(simulate_device_probe("router-01"))

	assert result == {
		"device_id": "router-01",
		"reachable": True,
		"simulated": True,
	}