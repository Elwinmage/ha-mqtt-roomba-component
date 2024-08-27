"""Constants for the X-Sense Home Security integration."""
import logging

DOMAIN = "mqttroomba"
MANUFACTURER = "iRobot"
COORDINATOR = "coordinator"

LOGGER = logging.getLogger(__package__)

# DEFAULT
DEFAULT_SCAN_INTERVAL = 5

# CONF
CONF_MQTT_HOSTNAME="hostname"
CONF_MQTT_PORT="port"
CONF_MQTT_USERNAME="username"
CONF_MQTT_PASSWORD="password"
