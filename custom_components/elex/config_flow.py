"""Config flow for ELEX component."""

import voluptuous as vol
from homeassistant.config_entries import ConfigEntry, ConfigFlow, OptionsFlowWithReload
from homeassistant.core import callback

from .const import (
    CONF_MARKET_AREA,
    CONF_TOKEN,
    CONF_DURATION,
    CONF_SURCHARGE_ABS,
    CONF_SURCHARGE_PERC,
    CONF_TAX,
    CONFIG_VERSION,
    DEFAULT_DURATION,
    DEFAULT_SURCHARGE_ABS,
    DEFAULT_SURCHARGE_PERC,
    DEFAULT_TAX,
    DOMAIN,
)
from .ELEX import Elex  # Make sure your API file is named ELEX.py and class is Elex

class ElexConfigFlow(ConfigFlow, domain=DOMAIN):
    """Component config flow."""

    VERSION = CONFIG_VERSION

    async def async_step_user(self, user_input=None):
        """Handle the start of the config flow."""
        if user_input is not None:
            market_area = user_input[CONF_MARKET_AREA]
            title = f"ELEX ({market_area})"

            unique_id = f"{DOMAIN} {market_area}"
            await self.async_set_unique_id(unique_id)
            self._abort_if_unique_id_configured()

            data = {CONF_MARKET_AREA: market_area, CONF_TOKEN: user_input[CONF_TOKEN]}
            options = {CONF_DURATION: user_input.get(CONF_DURATION, DEFAULT_DURATION)}

            return self.async_create_entry(title=title, data=data, options=options)

        data_schema = vol.Schema(
            {
                vol.Required(CONF_MARKET_AREA): vol.In(Elex.MARKET_AREAS),
                vol.Required(CONF_TOKEN): vol.Coerce(str),
                vol.Required(CONF_DURATION, default=DEFAULT_DURATION): vol.In(Elex.SUPPORTED_DURATIONS),
            }
        )

        return self.async_show_form(step_id="user", data_schema=data_schema)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> OptionsFlowWithReload:
        return ElexOptionsFlow()


class ElexOptionsFlow(OptionsFlowWithReload):
    """Handle the start of the option flow."""

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_SURCHARGE_PERC,
                        default=self.config_entry.options.get(CONF_SURCHARGE_PERC, DEFAULT_SURCHARGE_PERC),
                    ): vol.Coerce(float),
                    vol.Optional(
                        CONF_SURCHARGE_ABS,
                        default=self.config_entry.options.get(CONF_SURCHARGE_ABS, DEFAULT_SURCHARGE_ABS),
                    ): vol.Coerce(float),
                    vol.Optional(
                        CONF_TAX,
                        default=self.config_entry.options.get(CONF_TAX, DEFAULT_TAX),
                    ): vol.Coerce(float),
                    vol.Required(
                        CONF_DURATION,
                        default=self.config_entry.options.get(CONF_DURATION, DEFAULT_DURATION),
                    ): vol.In(Elex.SUPPORTED_DURATIONS),
                }
            ),
        )