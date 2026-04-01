"""Constants for the ELEX component."""

DOMAIN = "elex"

ATTR_DATA = "data"
ATTR_START_TIME = "start_time"
ATTR_END_TIME = "end_time"
ATTR_BUY_VOLUME_MWH = "buy_volume_mwh"
ATTR_SELL_VOLUME_MWH = "sell_volume_mwh"
ATTR_VOLUME_MWH = "volume_mwh"
ATTR_RANK = "rank"
ATTR_QUANTILE = "quantile"
ATTR_PRICE_PER_KWH = "price_per_kwh"

CONFIG_VERSION = 2
CONF_MARKET_AREA = "market_area"
CONF_TOKEN = "token"

# configuration options for total price calculation
CONF_SURCHARGE_PERC = "percentage_surcharge"
CONF_SURCHARGE_ABS = "absolute_surcharge"
CONF_TAX = "tax"

# service call
CONF_EARLIEST_START_TIME = "earliest_start"
CONF_EARLIEST_START_POST = "earliest_start_post"
CONF_LATEST_END_TIME = "latest_end"
CONF_LATEST_END_POST = "latest_end_post"
CONF_DURATION = "duration"

DEFAULT_SURCHARGE_PERC = 3.0
DEFAULT_SURCHARGE_ABS = 0.1193
DEFAULT_TAX = 19.0
DEFAULT_DURATION = 60

EMPTY_EXTREME_PRICE_INTERVAL_RESP = {
    "start": None,
    "end": None,
    "market_price_per_kwh": None,
    "total_price_per_kwh": None,
}

UOM_EUR_PER_KWH = "€/kWh"
UOM_MWH = "MWh"
EUR_PER_MWH = "EUR/MWh"
CT_PER_KWH = "ct/kWh"