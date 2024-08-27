"""Config flow for X-Sense Home Security integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError


import paho.mqtt.client as mqtt

from .const import (
    DOMAIN,
    CONF_MQTT_HOSTNAME,
    CONF_MQTT_PORT,
    CONF_MQTT_USERNAME,
    CONF_MQTT_PASSWORD)

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_MQTT_HOSTNAME): str,
        vol.Required(CONF_MQTT_PORT,default=1883): int,
        vol.Required(CONF_MQTT_USERNAME): str,
        vol.Required(CONF_MQTT_PASSWORD): str,
    }
)


async def validate_input(hass: HomeAssistant, hostname,port,username, password) -> dict[str, Any]:
    """Validate the user input allows us to connect.

    Data has the keys from STEP_USER_DATA_SCHEMA with values provided by the user.
    """
    try:
        mqttc = mqtt.Client("MQTTRommba")
        mqttc.username_pw_set(username,password)
        mqttc.connect(hostname, port, 60)
        mqttc.disconnect()
    except Exception as ex:
        raise InvalidAuth(f"Login failed: {str(ex)}") from ex
    # Return info that you want to store in the config entry.
    return {"title": f"MQTT {hostname}"}


class MQTTRoombaConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for X-Sense Home Security."""

    VERSION = 1
    entry: config_entries.ConfigEntry

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            hostname = user_input[CONF_MQTT_HOSTNAME] 
            port     = user_input[CONF_MQTT_PORT] 
            username = user_input[CONF_MQTT_USERNAME]
            password = user_input[CONF_MQTT_PASSWORD]
            try:
                info = await validate_input(self.hass, hostname, port,username, password)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                await self.async_set_unique_id(hostname)
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title=info["title"],
                    data={CONF_MQTT_HOSTNAME: hostname, CONF_MQTT_PORT: port, CONF_MQTT_USERNAME: username, CONF_MQTT_PASSWORD: password},
                )

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )

    async def async_step_reauth(self, user_input=None):
        """Perform reauth upon an API authentication error."""
        self.entry = self.hass.config_entries.async_get_entry(self.context["entry_id"])
        return await self.async_step_reauth_confirm()

    async def async_step_reauth_confirm(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle re-authentication with XSense."""
        errors: dict[str, str] = {}

        if user_input is not None:
            hostname = user_input[CONF_MQTT_HOSTNAME]
            port     = user_input[CONF_MQTT_PORT]
            username = user_input[CONF_MQTT_USERNAME]
            password = user_input[CONF_MQTT_PASSWORD]
            try:
                _ = await validate_input(self.hass, hostname, port,username, password)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                existing_entry = await self.async_set_unique_id(hostname)
                if existing_entry and self.entry:
                    self.hass.config_entries.async_update_entry(
                        existing_entry,
                        data={
                            **self.entry.data,
                            CONF_MQTT_HOSTNAME: hostname,
                            CONF_MQTT_PORT: port,
                            CONF_MQTT_USERNAME: username,
                            CONF_MQTT_PASSWORD: password,
                        },
                    )
                    await self.hass.config_entries.async_reload(existing_entry.entry_id)
                    return self.async_abort(reason="reauth_successful")

        return self.async_show_form(
            step_id="reauth_confirm",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_MQTT_HOSTNAME, default=self.entry.data[CONF_MQTT_HOSTNAME]): str,
                    vol.Required(CONF_MQTT_PORT, default=self.entry.data[CONF_MQTT_PORT]): str,
                    vol.Required(CONF_MQTT_USERNAME, default=self.entry.data[CONF_MQTT_USERNAME]): str,
                    vol.Required(CONF_MQTT_PASSWORD): str,
                }
            ),
            errors=errors,
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""
