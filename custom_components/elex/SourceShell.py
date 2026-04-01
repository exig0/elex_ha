"""SourceShell"""

from datetime import timedelta
import logging
from typing import Any
import aiohttp
from homeassistant.config_entries import ConfigEntry
from homeassistant.util import dt

from .const import (
    CONF_DURATION,
    CONF_EARLIEST_START_POST,
    CONF_EARLIEST_START_TIME,
    CONF_LATEST_END_POST,
    CONF_LATEST_END_TIME,
    CONF_MARKET_AREA,
    CONF_SURCHARGE_ABS,
    CONF_SURCHARGE_PERC,
    CONF_TAX,
    CONF_TOKEN,
    DEFAULT_DURATION,
    DEFAULT_SURCHARGE_ABS,
    DEFAULT_SURCHARGE_PERC,
    DEFAULT_TAX,
    EMPTY_EXTREME_PRICE_INTERVAL_RESP,
)
from .ELEX import Elex
from .extreme_price_interval import find_extreme_price_interval, get_start_times

_LOGGER = logging.getLogger(__name__)

class SourceShell:
    def __init__(self, config_entry: ConfigEntry, session: aiohttp.ClientSession):
        self._config_entry = config_entry
        self._marketdata_now = None
        self._sorted_marketdata_today = []
        
        self._source = Elex(
            market_area=config_entry.data[CONF_MARKET_AREA],
            api_key=config_entry.data[CONF_TOKEN],
            duration=config_entry.options.get(CONF_DURATION, DEFAULT_DURATION),
            session=session,
        )

    @property
    def unique_id(self):
        return self._config_entry.unique_id

    @property
    def name(self):
        return self._source.name

    @property
    def market_area(self):
        return self._source.market_area

    @property
    def duration(self):
        return self._source.duration

    @property
    def currency(self):
        return self._source.currency

    @property
    def marketdata(self):
        return self._source.marketdata

    @property
    def marketdata_now(self):
        return self._marketdata_now

    @property
    def sorted_marketdata_today(self):
        """Sorted by price."""
        return self._sorted_marketdata_today

    async def fetch(self, *args: Any):
        await self._source.fetch()

    def update_time(self):
        if (len(self.marketdata)) == 0:
            self._marketdata_now = None
            self._sorted_marketdata_today = []
            return

        now = dt.now()

        try:
            self._marketdata_now = next(
                filter(
                    lambda e: e.start_time <= now and e.end_time > now, self.marketdata
                )
            )
        except StopIteration:
            _LOGGER.error(f"no data found for {self._source.name}")
            self._marketdata_now = None
            self._sorted_marketdata_today = []

        start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day + timedelta(days=1)

        sorted_marketdata_today = filter(
            lambda e: e.start_time >= start_of_day and e.end_time <= end_of_day,
            self.marketdata,
        )
        self._sorted_marketdata_today = sorted(
            sorted_marketdata_today, key=lambda e: e.market_price_per_kwh
        )

    def to_total_price(self, market_price_per_kwh):
        total_price = market_price_per_kwh

        surcharge_abs = self._config_entry.options.get(CONF_SURCHARGE_ABS, DEFAULT_SURCHARGE_ABS)
        tax = self._config_entry.options.get(CONF_TAX, DEFAULT_TAX)
        surcharge_pct = self._config_entry.options.get(CONF_SURCHARGE_PERC, DEFAULT_SURCHARGE_PERC)

        total_price = total_price + abs(total_price) * surcharge_pct / 100
        total_price += surcharge_abs
        total_price *= 1 + (tax / 100.0)

        return round(total_price, 6)

    def find_extreme_price_interval(self, call_data, cmp):
        duration: timedelta = call_data[CONF_DURATION]

        start_times = get_start_times(
            marketdata=self.marketdata,
            earliest_start_time=call_data.get(CONF_EARLIEST_START_TIME),
            earliest_start_post=call_data.get(CONF_EARLIEST_START_POST),
            latest_end_time=call_data.get(CONF_LATEST_END_TIME),
            latest_end_post=call_data.get(CONF_LATEST_END_POST),
            latest_market_datetime=self.marketdata[-1].end_time,
            duration=duration,
        )

        result = find_extreme_price_interval(
            self.marketdata, start_times, duration, cmp
        )

        if result is None:
            return EMPTY_EXTREME_PRICE_INTERVAL_RESP

        return {
            "start": result["start"],
            "end": result["start"] + duration,
            "market_price_per_kwh": round(result["market_price_per_hour"], 6),
            "total_price_per_kwh": self.to_total_price(result["market_price_per_hour"]),
        }