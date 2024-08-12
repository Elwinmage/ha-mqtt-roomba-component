import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN
import logging


PLATFORMS = ["sensor"]
_LOGGER = logging.getLogger(__name__)


class MQTTRoombaConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """MQTTRoomba config flow."""
    # The schema version of the entries that it creates
    # Home Assistant will call your migrate method if the version changes
    VERSION = 1
    MINOR_VERSION = 0


    async def async_step_user(self, user_input: dict | None = None):
        """Gestion de l'étape 'user'. Point d'entrée de notre
        """
        user_form = vol.Schema({vol.Required("Name"): str})

        if user_input is None:
            _LOGGER.debug(
                "config_flow step user (1). 1er appel : pas de user_input -> on affiche le form user_form"
            )
            return self.async_show_form(step_id="user", data_schema=user_form)

        # 2ème appel : il y a des user_input -> on stocke le résultat
        # TODO: utiliser les user_input
        _LOGGER.debug(
            "config_flow step user (2). On a reçu les valeurs: %s", user_input
        )



