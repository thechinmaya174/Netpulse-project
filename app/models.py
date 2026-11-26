from datetime import datetime
from ipaddress import IPv4Address
from typing import Literal

from pydantic import BaseModel, ConfigDict


DeviceType = Literal["router", "switch", "server"]
DeviceStatus = Literal["online", "offline"]


class DeviceCreate(BaseModel):
	model_config = ConfigDict(
		json_schema_extra={
			"examples": [
				{
					"device_id": "router-01",
					"name": "Main router",
					"device_type": "router",
					"ip_address": "192.168.1.10",
					"status": "online",
				}
			]
		}
	)

	device_id: str
	name: str
	device_type: DeviceType
	ip_address: IPv4Address
	status: DeviceStatus = "online"


class DeviceResponse(BaseModel):
	device_id: str
	name: str
	device_type: DeviceType
	ip_address: IPv4Address
	status: DeviceStatus


class StatusUpdate(BaseModel):
	model_config = ConfigDict(json_schema_extra={"examples": [{"status": "offline"}]})

	status: DeviceStatus


class AlertResponse(BaseModel):
	device_id: str
	message: str
	timestamp: datetime


class HealthResponse(BaseModel):
	status: Literal["ok"]
