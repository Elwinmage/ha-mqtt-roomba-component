"""DataUpdateCoordinator for the XSense integration."""
from __future__ import annotations

from datetime import timedelta
from typing import Any

import logging
import json

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
        self.mqttc = mqtt.Client("MQTTRommba")
        self.unique_id = "MQTTROOMBAUID"

        threading.Thread.__init__(self, name=self.unique_id)

    def run(self) -> None:
        hostname = self.entry.data[CONF_MQTT_HOSTNAME]
        port     = self.entry.data[CONF_MQTT_PORT]
        username = self.entry.data[CONF_MQTT_USERNAME]
        password = self.entry.data[CONF_MQTT_PASSWORD]

        self.mqttc.on_connect = on_connect
        self.mqttc.on_message = on_message
        self.mqttc.username_pw_set(username, password)

        _LOGGER.error("Let's go!")
        try:
            self.mqttc.connect(hostname,port, 60)
        except AuthFailed as ex:
            raise ConfigEntryAuthFailed(f"Login failed: {str(ex)}") from ex
        LOGGER.debug("Logged in")
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
            _LOGGER.error("Roomba Room: "+str(room))
            room_id = room["id"]
            room_name= room["name"]
    elif msg.topic == "/roomba/feedback/state":
        
        _LOGGER.info("Roomba State: "+str(msg.payload))
    else:
        _LOGGER.error("Topic "+msg.topic+" not implemented")

        
