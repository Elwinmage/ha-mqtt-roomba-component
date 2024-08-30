"""DataUpdateCoordinator for the XSense integration."""
from __future__ import annotations

from datetime import timedelta
from typing import Any

import logging
import json
import asyncio

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed

import threading

import paho.mqtt.client as mqtt

from .const import (
    DOMAIN,
    LOGGER,
    CONF_MQTT_HOSTNAME,
    CONF_MQTT_PORT,
    CONF_MQTT_USERNAME,
    CONF_MQTT_PASSWORD,
    DEFAULT_SCAN_INTERVAL)

_LOGGER = logging.getLogger(__name__)

class MQTTRoombaDataUpdateCoordinator(threading.Thread):
    """A MQTT Roomba Data Update Coordinator."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the Roomba hub."""
        self._run = False
        self.entry = entry
        self._hass = hass
        self.mqttc = mqtt.Client("MQTTRommba")
        self.unique_id = "MQTTROOMBAUID"
        self._entities = {}
        self._initialized = False
        threading.Thread.__init__(self, name=self.unique_id)

    def run(self) -> None:
        hostname = self.entry.data[CONF_MQTT_HOSTNAME]
        port     = self.entry.data[CONF_MQTT_PORT]
        username = self.entry.data[CONF_MQTT_USERNAME]
        password = self.entry.data[CONF_MQTT_PASSWORD]

        
        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_message = self.on_message
        self.mqttc.username_pw_set(username, password)

        #self.entity_state = MQTTRoombaSensorEntity()
        _LOGGER.error("Let's go!")
        try:
            self.mqttc.connect(hostname,port, 60)
        except AuthFailed as ex:
            raise ConfigEntryAuthFailed(f"Login failed: {str(ex)}") from ex
        LOGGER.debug("Logged in")
        self.mqttc.loop_forever()

    def register_entity(self,entity):
        self._entities[entity.name] = entity
        _LOGGER.error("adding entity: %s"%entity.name)

    def initialized(self):
        self._initialized = True
        
    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, userdata, flags, reason_code): #, properties):
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe("/roomba/#")

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        if msg.topic == "/roomba/rooms":
            rooms=json.loads(msg.payload)
            for room in rooms:
                _LOGGER.error("Roomba Room: "+str(room))
                room_id = room["id"]
                room_name= room["name"]
        elif msg.topic == "/roomba/feedback/state" and self._initialized:
            _LOGGER.error("search  entity: %s",msg.topic[1:].replace("/","_"))
            try:
                entity = self._entities[msg.topic[1:].replace("/","_")]
                asyncio.run_coroutine_threadsafe(entity.async_push_update(msg.payload), self._hass.loop)
            except:
                _LOGGER.error("Uninitialized Coordinator!")
                _LOGGER.error(self._entities)
        else:
            pass
        #_LOGGER.warning("Topic "+msg.topic+" not implemented")
        #name  = '_'.join(msg.topic.split('/')[2:])



        
