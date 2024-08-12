"""Constants for integration."""

NAME = "MQTT for Roomba"
DOMAIN = "mqttroomba"
DOMAIN_DATA = f"{DOMAIN}_data"
VERSION = "2024.08.12"
ISSUE_URL = "https://github.com/Elwinmage/ha-mqtt-roomba-component/issues"

PLATFORMS = ["sensor"]

# Defaults
DEFAULT_NAME = DOMAIN

STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
This is a custom integration!
If you have any issues with this you need to open an issue here:
{ISSUE_URL}
-------------------------------------------------------------------
"""
