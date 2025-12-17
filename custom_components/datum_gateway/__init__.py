"""The DATUM Gateway integration."""
from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN
from .datum_api import DatumGatewayAPI

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up DATUM Gateway from a config entry."""
    host = entry.data["host"]
    verify_ssl = entry.data.get("verify_ssl", False)
    
    # Create API instance
    api = DatumGatewayAPI(host, verify_ssl)
    
    # Create coordinator
    coordinator = DatumGatewayCoordinator(hass, api)
    
    # Fetch initial data
    await coordinator.async_config_entry_first_refresh()
    
    # Store coordinator
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator
    
    # Forward setup to platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)
    
    return unload_ok


class DatumGatewayCoordinator(DataUpdateCoordinator):
    """Class to manage fetching DATUM Gateway data."""

    def __init__(self, hass: HomeAssistant, api: DatumGatewayAPI) -> None:
        """Initialize."""
        self.api = api
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=30),
        )

    async def _async_update_data(self):
        """Fetch data from API endpoint."""
        try:
            # Fetch from main status page
            status_data = await self.hass.async_add_executor_job(
                self.api.get_status
            )
            
            # Fetch from threads page
            threads_data = await self.hass.async_add_executor_job(
                self.api.get_threads
            )
            
            # Combine data
            return {
                "status": status_data,
                "threads": threads_data,
            }
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}")
