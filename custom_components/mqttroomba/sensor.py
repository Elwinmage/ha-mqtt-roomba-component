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

import logging
_LOGGER = logging.getLogger(__name__) 

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
    discovery_info=None,  # pylint: disable=unused-argument
):
    """Configuration de la plate-forme tuto_hacs à partir de la configuration
    trouvée dans configuration.yaml"""

    _LOGGER.debug("Calling async_setup_platform entry=%s", entry)
    coordinator: MQTTRoombaDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    
    entity = MQTTRoombaSensorEntity(hass, "roomba_feedback_state",coordinator)
    async_add_entities([entity], True)
    coordinator.initialized()
    
class MQTTRoombaSensorEntity(SensorEntity):
    """Representation of a roomba device."""

    #entity_description: MQTTRoombaSensorEntityDescription

    def __init__(
        self,
        hass: HomeAssistant,    
        name,
        coordinator: MQTTRoombaDataUpdateCoordinator,
 #       entity: Entity,
#        entity_description: MQTTRoombaSensorEntityDescription,
    ) -> None:
        """Set up the instance."""
#        self.entity_description = entity_description
        self._attr_available = False  # This overrides the default
        self._attr_name = name
        self._attr_unique_id = "sensor."+name
        self._attr_has_entity_name = True        
        self._coordinator = coordinator
        #super().__init__(coordinator, entity)
        self._coordinator.register_entity(self)
        self._attr_native_value = None
        self._options = ["Charging","Cleaning"]
        
        
    def set_state(self, state):
        self._attr_native_value = state


    async def async_push_update(self, state):
        """Update the sensor state."""
        self._attr_native_value = str(state)
        self.async_write_ha_state()       

    @property
    def name(self):
        """Return the name of the entity."""
        return self._attr_name

    @property
    def icon(self) -> str | None:
        return "mdi:sine-wave"

    # @property
    # def device_class(self) -> SensorDeviceClass | None:
    #     return SensorDeviceClass.ENUM

    @property
    def options(self):
        return ', '.join(self._options)

