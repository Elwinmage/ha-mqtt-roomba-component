"""Constants for integration."""

NAME = "MQTT for Roomba"
DOMAIN = "mqttroomba"
DOMAIN_DATA = f"{DOMAIN}_data"
DEVICE_MANUFACTURER = "iRobot"
VERSION = "2024.08.12"
ISSUE_URL = "https://github.com/Elwinmage/ha-mqtt-roomba-component/issues"

PLATFORMS = ["sensor"]

# Defaults
DEFAULT_NAME = DOMAIN

# CONF
CONF_MQTT_HOSTNAME="hostname"
CONF_MQTT_PORT="port"
CONF_MQTT_USERNAME="username"
CONF_MQTT_PASSWORD="password"

STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
This is a custom integration!
If you have any issues with this you need to open an issue here:
{ISSUE_URL}
-------------------------------------------------------------------
"""
