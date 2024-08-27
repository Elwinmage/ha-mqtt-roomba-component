"""Support for xsense sensors."""

from __future__ import annotations


from homeassistant import config_entries
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import MQTTRoombaDataUpdateCoordinator

async def async_setup_entry(
    hass: HomeAssistant,
    entry: config_entries.ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the xsense sensor entry."""
    devices: list[Device] = []
    coordinator: MQTTRoombaDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    #TODO add entities
    async_add_entities(devices)


class MQTTRoombaSensorEntity(SensorEntity):
    """Representation of a roomba device."""

    #entity_description: MQTTRoombaSensorEntityDescription

    def __init__(
        self,
        coordinator: MQTTRoombaDataUpdateCoordinator,
        entity: Entity,
        entity_description: MQTTRoombaSensorEntityDescription,
    ) -> None:
        """Set up the instance."""
        self.entity_description = entity_description
        self._attr_available = False  # This overrides the default

        #super().__init__(coordinator, entity)

