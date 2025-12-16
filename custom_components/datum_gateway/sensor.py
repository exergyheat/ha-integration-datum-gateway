"""Sensor platform for DATUM Gateway."""
from __future__ import annotations

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfDataRate
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up DATUM Gateway sensors from config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    
    # Create sensor entities
    entities = [
        # Mining Performance Sensors
        DatumTotalHashrateSensor(coordinator, entry),
        DatumSharesAcceptedSensor(coordinator, entry),
        DatumSharesRejectedSensor(coordinator, entry),
        DatumAcceptanceRateSensor(coordinator, entry),
        
        # Pool Status Sensors
        DatumPoolStatusSensor(coordinator, entry),
        DatumPoolHostSensor(coordinator, entry),
        DatumMinerTagSensor(coordinator, entry),
        
        # System Sensors
        DatumActiveThreadsSensor(coordinator, entry),
        DatumConnectionsSensor(coordinator, entry),
        DatumUptimeSensor(coordinator, entry),
        
        # Block Template Sensors
        DatumBlockHeightSensor(coordinator, entry),
        DatumBlockValueSensor(coordinator, entry),
        DatumTransactionCountSensor(coordinator, entry),
    ]
    
    # Add thread-specific sensors
    if "threads" in coordinator.data and "threads" in coordinator.data["threads"]:
        for thread in coordinator.data["threads"]["threads"]:
            entities.append(DatumThreadHashrateSensor(coordinator, entry, thread["tid"]))
    
    async_add_entities(entities)


class DatumSensorBase(CoordinatorEntity, SensorEntity):
    """Base class for DATUM Gateway sensors."""

    def __init__(self, coordinator, entry: ConfigEntry) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_has_entity_name = True
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": "DATUM Gateway",
            "manufacturer": "OCEAN.xyz",
            "model": "DATUM Gateway",
        }


class DatumTotalHashrateSensor(DatumSensorBase):
    """Sensor for total hashrate."""

    _attr_name = "Total Hashrate"
    _attr_unique_id_suffix = "total_hashrate"
    _attr_native_unit_of_measurement = "TH/s"
    _attr_device_class = SensorDeviceClass.DATA_RATE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_icon = "mdi:chip"

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self.coordinator.config_entry.entry_id}_{self._attr_unique_id_suffix}"

    @property
    def native_value(self):
        """Return the state."""
        return self.coordinator.data.get("status", {}).get("total_hashrate")


class DatumSharesAcceptedSensor(DatumSensorBase):
    """Sensor for shares accepted."""

    _attr_name = "Shares Accepted"
    _attr_unique_id_suffix = "shares_accepted"
    _attr_state_class = SensorStateClass.TOTAL_INCREASING
    _attr_icon = "mdi:check-circle"

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self.coordinator.config_entry.entry_id}_{self._attr_unique_id_suffix}"

    @property
    def native_value(self):
        """Return the state."""
        return self.coordinator.data.get("status", {}).get("shares_accepted")


class DatumSharesRejectedSensor(DatumSensorBase):
    """Sensor for shares rejected."""

    _attr_name = "Shares Rejected"
    _attr_unique_id_suffix = "shares_rejected"
    _attr_state_class = SensorStateClass.TOTAL_INCREASING
    _attr_icon = "mdi:close-circle"

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self.coordinator.config_entry.entry_id}_{self._attr_unique_id_suffix}"

    @property
    def native_value(self):
        """Return the state."""
        return self.coordinator.data.get("status", {}).get("shares_rejected")


class DatumAcceptanceRateSensor(DatumSensorBase):
    """Sensor for share acceptance rate."""

    _attr_name = "Acceptance Rate"
    _attr_unique_id_suffix = "acceptance_rate"
    _attr_native_unit_of_measurement = "%"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_icon = "mdi:percent"

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self.coordinator.config_entry.entry_id}_{self._attr_unique_id_suffix}"

    @property
    def native_value(self):
        """Return the state."""
        return self.coordinator.data.get("status", {}).get("acceptance_rate")


class DatumPoolStatusSensor(DatumSensorBase):
    """Sensor for pool connection status."""

    _attr_name = "Pool Status"
    _attr_unique_id_suffix = "pool_status"
    _attr_icon = "mdi:lan-connect"

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self.coordinator.config_entry.entry_id}_{self._attr_unique_id_suffix}"

    @property
    def native_value(self):
        """Return the state."""
        return self.coordinator.data.get("status", {}).get("pool_status")


class DatumPoolHostSensor(DatumSensorBase):
    """Sensor for pool host."""

    _attr_name = "Pool Host"
    _attr_unique_id_suffix = "pool_host"
    _attr_icon = "mdi:server-network"
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self.coordinator.config_entry.entry_id}_{self._attr_unique_id_suffix}"

    @property
    def native_value(self):
        """Return the state."""
        return self.coordinator.data.get("status", {}).get("pool_host")


class DatumMinerTagSensor(DatumSensorBase):
    """Sensor for miner tag."""

    _attr_name = "Miner Tag"
    _attr_unique_id_suffix = "miner_tag"
    _attr_icon = "mdi:tag"
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self.coordinator.config_entry.entry_id}_{self._attr_unique_id_suffix}"

    @property
    def native_value(self):
        """Return the state."""
        return self.coordinator.data.get("status", {}).get("miner_tag")


class DatumActiveThreadsSensor(DatumSensorBase):
    """Sensor for active threads."""

    _attr_name = "Active Threads"
    _attr_unique_id_suffix = "active_threads"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_icon = "mdi:cpu-64-bit"

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self.coordinator.config_entry.entry_id}_{self._attr_unique_id_suffix}"

    @property
    def native_value(self):
        """Return the state."""
        return self.coordinator.data.get("status", {}).get("active_threads")


class DatumConnectionsSensor(DatumSensorBase):
    """Sensor for total connections."""

    _attr_name = "Total Connections"
    _attr_unique_id_suffix = "total_connections"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_icon = "mdi:lan"

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self.coordinator.config_entry.entry_id}_{self._attr_unique_id_suffix}"

    @property
    def native_value(self):
        """Return the state."""
        return self.coordinator.data.get("status", {}).get("total_connections")


class DatumUptimeSensor(DatumSensorBase):
    """Sensor for uptime."""

    _attr_name = "Uptime"
    _attr_unique_id_suffix = "uptime"
    _attr_icon = "mdi:clock-outline"
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self.coordinator.config_entry.entry_id}_{self._attr_unique_id_suffix}"

    @property
    def native_value(self):
        """Return the state."""
        return self.coordinator.data.get("status", {}).get("uptime")


class DatumBlockHeightSensor(DatumSensorBase):
    """Sensor for block height."""

    _attr_name = "Block Height"
    _attr_unique_id_suffix = "block_height"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_icon = "mdi:cube-outline"

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self.coordinator.config_entry.entry_id}_{self._attr_unique_id_suffix}"

    @property
    def native_value(self):
        """Return the state."""
        return self.coordinator.data.get("status", {}).get("block_height")


class DatumBlockValueSensor(DatumSensorBase):
    """Sensor for block value."""

    _attr_name = "Block Value"
    _attr_unique_id_suffix = "block_value"
    _attr_native_unit_of_measurement = "BTC"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_icon = "mdi:bitcoin"

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self.coordinator.config_entry.entry_id}_{self._attr_unique_id_suffix}"

    @property
    def native_value(self):
        """Return the state."""
        return self.coordinator.data.get("status", {}).get("block_value")


class DatumTransactionCountSensor(DatumSensorBase):
    """Sensor for transaction count."""

    _attr_name = "Transaction Count"
    _attr_unique_id_suffix = "transaction_count"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_icon = "mdi:swap-horizontal"

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self.coordinator.config_entry.entry_id}_{self._attr_unique_id_suffix}"

    @property
    def native_value(self):
        """Return the state."""
        return self.coordinator.data.get("status", {}).get("transaction_count")


class DatumThreadHashrateSensor(DatumSensorBase):
    """Sensor for individual thread hashrate."""

    def __init__(self, coordinator, entry: ConfigEntry, tid: int) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, entry)
        self._tid = tid
        self._attr_name = f"Thread {tid} Hashrate"
        self._attr_unique_id_suffix = f"thread_{tid}_hashrate"
        self._attr_native_unit_of_measurement = "TH/s"
        self._attr_device_class = SensorDeviceClass.DATA_RATE
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_icon = "mdi:chip"

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self.coordinator.config_entry.entry_id}_{self._attr_unique_id_suffix}"

    @property
    def native_value(self):
        """Return the state."""
        threads = self.coordinator.data.get("threads", {}).get("threads", [])
        for thread in threads:
            if thread.get("tid") == self._tid:
                return thread.get("hashrate")
        return None
