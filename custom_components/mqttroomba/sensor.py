""" Implements the Tuto HACS sensors component """
import logging

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry


from homeassistant.helpers.entity_platform import (
    AddEntitiesCallback,
    async_get_current_platform,
)
from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo


from .const import (
    DOMAIN,
    DEVICE_MANUFACTURER)

from . import async_get_or_create

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
    discovery_info=None,  # pylint: disable=unused-argument
):
    _LOGGER.debug("Calling async_setup_entry entry=%s", entry)

    entity = RoombaSensor(hass, entry)
    async_add_entities([entity], True)
    platform = async_get_current_platform()
    await async_get_or_create(hass, entity  )


class RoombaSensorState(SensorEntity):
    """La classe de l'entité ADS1115Sensor"""

    def __init__(
        self,
        hass: HomeAssistant,  # pylint: disable=unused-argument
    ) -> None:
        """Initisalisation de notre entité"""
        self._state=None
        self._hass = hass
        self._entry_infos=entry_infos
        self._attr_has_entity_name = True
        self._attr_name = 'State'
    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        return DeviceInfo(
            entry_type=DeviceEntryType.SERVICE,
            identifiers={(DOMAIN,"State")},
            name="Roomba",
#            identifiers={(DOMAIN,self._device_id)},
#            name=self._device_id,
            manufacturer=DEVICE_MANUFACTURER,
            model=DOMAIN,
        )

    @property
    def readRequest(self):
        """Return bytes to send for reading"""
        return self._read_request
        
    @property
    def unique_id(self):
        """Return unique id"""
        return f"sensor.RoombaSenrorState"

    def set_state(self,state):
        """Set state"""
        self._state = state
        _LOGGER.debug("%s:%f"%(self.unique_id,state))
        
    @property
    def state(self):
        """Returns state of the sensor."""
        return self._state

    @property
    def should_poll(self) -> bool:
        """Poll for those entities"""
        return True

    @property
    def icon(self) -> str | None:
        return "mdi:sine-wave"

    
    # def state_class(self) -> SensorStateClass | None:
    #     return SensorStateClass.MEASUREMENT

    # @property
    # def native_unit_of_measurement(self) -> str | None:
    #     return UnitOfElectricPotential.VOLT

