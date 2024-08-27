"""Custom integration to integrate Roomba with Home Assistant.

For more details about this integration, please refer to
https://github.com/Elwinmage/ha-mqtt-roomba-component
"""
from datetime import timedelta
import logging
import threading
import functools
import asyncio
import json

import paho.mqtt.client as mqtt

from homeassistant.core import Config, HomeAssistant
from homeassistant.const import Platform
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN, STARTUP_MESSAGE
from homeassistant.const import EVENT_HOMEASSISTANT_START, EVENT_HOMEASSISTANT_STOP

SCAN_INTERVAL = timedelta(seconds=30)

_LOGGER: logging.Logger = logging.getLogger(__package__)

PLATFORMS: list[Platform] = ["sensor"]


class iRobot(threading.Thread):
    def __init__(self, hass):
        self._run= False
        self.unique_id = "ROOMBAUID"
        self.mqttc = None
        threading.Thread.__init__(self, name=self.unique_id)
        self.entity_state = RoombaSensorState(hass)
        
        
    def start_polling(self):
        """Start polling thread."""
        self._run = True
        self.start()
    
    def run(self):
        _LOGGER.info("let's go!")
        # # The callback for when the client receives a CONNACK response from the server.
        # def on_connect(client, userdata, flags, reason_code, properties):
        #     # Subscribing in on_connect() means that if we lose the connection and
        #     # reconnect then subscriptions will be renewed.
        #     client.subscribe("/roomba/#")

        # # The callback for when a PUBLISH message is received from the server.
        # def on_message(client, userdata, msg):
        #     _LOGGER.error(msg.topic+" "+str(msg.payload))

        self.mqttc = mqtt.Client("MQTTRommba")
        self.mqttc.on_connect = on_connect
        self.mqttc.on_message = on_message
        self.mqttc.username_pw_set("MQTT", "42134213")
        self.mqttc.connect("192.168.0.109", 1883, 60)
        self.mqttc.loop_forever()

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, reason_code): #, properties):
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("/roomba/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    if msg.topic == "/roomba/rooms":
        rooms=json.loads(msg.payload)
        for room in rooms:
            _LOGGER.info("Roomba Room: "+str(room))
            room_id = room["id"]
            room_name= room["name"]
            
            
    elif msg.topic == '/roomba/feedback/state':
        
        _LOGGER.info("Roomba State: "+str(msg.payload))
    else:
        _LOGGER.error("Topic "+msg.topic+" not implemented")


async def update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Fonction qui force le rechargement des entités associées à une configEntry"""
    await hass.config_entries.async_reload(entry.entry_id)
        
async def async_get_or_create(hass, entity):
    """Get or create a MCP23017 component from entity bus and i2c address."""

    if 'Roomba' in  hass.data[DOMAIN]:
        component = hass.data[DOMAIN]['Roomba']
    else:
        # Try to create component when it doesn't exist
        component = await hass.async_add_executor_job(
            functools.partial(iRobot, hass)
            )
        hass.data[DOMAIN]['Roomba'] = component
    return component


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Creation des entités à partir d'une configEntry"""

    _LOGGER.debug(
        "Appel de async_setup_entry entry: entry_id='%s', data='%s'",
        entry.entry_id,
        entry.data,
    )

    hass.data.setdefault(DOMAIN, {})
    entry.async_on_unload(entry.add_update_listener(update_listener))
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

   # Callback function to start polling when HA start
    def start_polling(event):
        for component in hass.data[DOMAIN].values():
            if not component.is_alive():
                component.start_polling()

    # Callback function to stop polling when HA stops
    def stop_polling(event):
        for component in hass.data[DOMAIN].values():
            if component.is_alive():
                component.stop_polling()
    return True

        
async def async_setup(hass: HomeAssistant, Config: Config) -> bool:
    

    _LOGGER.info(
        "Initializing %s integration with plaforms: %s with config: %s",
        DOMAIN,
        PLATFORMS,
        Config,
    )
    hass.data.setdefault(DOMAIN, {})
    async def start_polling(event):
        if 'Roomba' not in hass.data[DOMAIN]:
            component = await async_get_or_create(hass,None)
        else:
            component =  hass.data[DOMAIN]['Roomba'] 
        component.start_polling()
    
 
    # Mettre ici un eventuel code permettant l'initialisation de l'intégration
    # Ca peut être une connexion sur le Cloud qui fournit les données par ex
    # (pas nécessaire pour le tuto)

    # L'argument config contient votre fichier configuration.yaml
    my_config = Config.get(DOMAIN)  # pylint: disable=unused-variable

    hass.bus.async_listen_once(EVENT_HOMEASSISTANT_START, start_polling)

    # Return boolean to indicate that initialization was successful.
    return True
