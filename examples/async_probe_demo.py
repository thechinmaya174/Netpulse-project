import asyncio
import time

from app.services.probe import simulate_device_probe


DEVICE_IDS = ["router-01", "switch-01", "server-01"]


async def main() -> None:
	start = time.perf_counter()
	sequential_results = []
	for device_id in DEVICE_IDS:
		sequential_results.append(await simulate_device_probe(device_id))
	sequential_elapsed = time.perf_counter() - start

	start = time.perf_counter()
	concurrent_results = await asyncio.gather(
		*(simulate_device_probe(device_id) for device_id in DEVICE_IDS)
	)
	concurrent_elapsed = time.perf_counter() - start

	print("Sequential results:", sequential_results)
	print(f"Sequential elapsed: {sequential_elapsed:.3f} seconds")
	print("Concurrent results:", concurrent_results)
	print(f"Concurrent elapsed: {concurrent_elapsed:.3f} seconds")


if __name__ == "__main__":
	asyncio.run(main())