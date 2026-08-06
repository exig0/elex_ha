# ELEX Home Assistant Integration

## Application overview

This repository provides the `elex` custom integration for Home Assistant. It retrieves
day-ahead electricity spot prices from the ELEX API for a configured European market
area, converts the API's EUR/MWh values to EUR/kWh, and exposes the data to Home
Assistant for energy-aware automations.

The integration provides:

- A config flow for market area, API token, and price-slot duration.
- Options for percentage surcharge, absolute surcharge, and tax, used to calculate a
  total electricity price.
- Coordinator-backed sensor entities for current market and total prices, daily
  low/high/average/median prices, current price rank, and quantile.
- Services to refresh API data and find the lowest or highest price interval within a
  user-specified time range.

## Repository layout

- `custom_components/elex/__init__.py`: Home Assistant entry setup, coordinator,
  service registration, migration, and shared entity base class.
- `custom_components/elex/config_flow.py`: Config entry and options flows.
- `custom_components/elex/SourceShell.py`: Adapter between Home Assistant state and
  the ELEX client; maintains current and sorted daily market data and applies price
  adjustments.
- `custom_components/elex/ELEX/__init__.py`: Async ELEX HTTP client, market-area map,
  timestamp construction, and EUR/MWh-to-EUR/kWh conversion.
- `custom_components/elex/sensor.py`: Sensor entity implementations.
- `custom_components/elex/extreme_price_interval.py`: Pure interval-search and
  interval-price calculations.
- `custom_components/elex/const.py`: Domain, config, attribute, unit, and default
  values.
- `custom_components/elex/translations/en.json` and `services.yaml`: Home Assistant
  UI metadata. Keep them aligned with config-flow and service changes.
- `README.md`: User-facing installation, sensor, and service documentation.

## Implementation guidance

- Treat this as an asynchronous Home Assistant integration. Use Home Assistant's
  shared `aiohttp` client session and avoid blocking I/O in integration code.
- Keep the data flow intact: `Elex.fetch()` obtains and normalizes API data;
  `SourceShell` derives current/day-level state and total prices; the coordinator
  refreshes entities; sensor entities only expose coordinator/source state.
- ELEX prices returned by the API are EUR/MWh. Preserve the conversion to EUR/kWh
  (`/ 1000`) and round public price values to six decimal places.
- Use timezone-aware datetimes. The ELEX client requests dates in `Europe/Berlin`;
  Home Assistant-facing values should use `homeassistant.util.dt` helpers.
- Preserve the configured market-area value through the config flow, `SourceShell`,
  and the API request. Add a market only by updating `Elex.MARKET_AREAS`.
- When adding or changing config options, update `const.py`, the config/options
  schema, English translations, defaults, and README when user-visible behavior
  changes.
- When adding or changing services, update the Voluptuous schema and registration in
  `__init__.py`, `services.yaml`, translations, and README together. Services that
  select an integration instance should continue supporting Home Assistant
  `device_id` targeting.
- Sensors use Home Assistant's `SensorEntityDescription`, stable unique IDs, and the
  shared `ElexSpotEntity` base. New historical arrays should remain excluded from the
  recorder when appropriate via `_unrecorded_attributes`.
- Do not log API tokens or raw credentials. Surface API/network failures so Home
  Assistant can mark an entry unavailable or retry setup.

## Change and validation expectations

- Keep changes focused on the `elex` domain and preserve existing entity IDs,
  configuration keys, and service names unless a migration is included.
- Place deterministic logic in testable helper functions, especially for price,
  timezone, and interval calculations.
- `custom_components/elex/test_elex.py` is a manual API smoke script that requires
  network access; do not use it as a unit test or introduce real API credentials.
- Update `README.md` for user-visible sensors, configuration, service, or API
  behavior changes.
