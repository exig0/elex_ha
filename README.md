# ELEX Home Assistant Integration

[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/exig0/elex_ha)

This component adds real-time electricity prices, forecasts, and grid data from the [ELEX](https://elex.mk) platform to Home Assistant. ELEX provides day-ahead electricity price data for 49 European markets, empowering you to automate your smart home based on actual energy spot prices.

> **Note:** To use this integration, you need an API key. You can create a free account and generate your key at [elex.mk](https://elex.mk).

---

## Installation

1. Ensure that [HACS](https://hacs.xyz) is installed.

2. Go to **HACS** -> **Integrations** -> Click the three dots (top right) -> **Custom repositories**.
3. Add `https://github.com/exig0/elex_ha` and select **Integration** as the category.

4. Search for **ELEX** in HACS and click **Download**.

5. Restart Home Assistant.

6. Add the **ELEX** integration to your instance:

   [![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start?domain=elex)

## Sensors

This integration provides the following sensors:

1. Total price
2. Market price
3. Average market price during the day
4. Median market price during the day
5. Lowest market price during the day
6. Highest market price during the day
7. Current market price quantile during the day
8. Rank of the current market price during the day

### 1. Total Price Sensor

The sensor value reports the total market price in €/kWh. The price value will be updated every hour to reflect the current total market price.

The sensor attributes contain a list of all available total market prices (for today and tomorrow if available) in €/kWh.

```yaml
data:
  - start_time: "2026-04-01T23:00:00+00:00"
    end_time: "2026-04-02T00:00:00+00:00"
    price_per_kwh: 0.12485
  - start_time: "2026-04-02T00:00:00+00:00"
    end_time: "2026-04-02T01:00:00+00:00"
    price_per_kwh: 0.12235
  - start_time: "2026-04-02T01:00:00+00:00"
    end_time: "2026-04-02T02:00:00+00:00"
    price_per_kwh: 0.12247
```

The total market price will be calculated as follows:
`<Total Price>` = `<Market Price>` + `<Surcharges>` + `<Tax>`

- Total price is the price you have to pay at the end, including taxes, surcharges and VAT.
- Market price is the energy price from ELEX excluding taxes, surcharges, VAT.
- 2 different types of surcharges can be adjusted:
  1. Percentage Surcharge, stated in % of the ELEX market price.
  2. Absolute Surcharge, stated in €/kWh, excluding VAT.
- Tax, e.g. VAT

The values for surcharges and tax can be adjusted in the integration configuration.

Example:

```text
Percentage Surcharge = 3%
Absolute Surcharge = 0.012 €/kWh
Tax = 19%

Total Price = ((Market Price * 1.03) + 0.012) * 1.19
```

### 2. Market Price Sensor

The sensor value reports the ELEX market price in €/kWh. The market price doesn't include taxes, surcharges, or VAT. The price value will be updated every selected period to reflect the current market price.

The sensor attributes contain additional values:

- The market price in €/kWh.
- A list of all available market prices (for today and tomorrow if available) in €/kWh.

```yaml
market_price_per_kwh: 0.089958
data:
  - start_time: "2026-04-01T23:00:00+00:00"
    end_time: "2026-04-02T00:00:00+00:00"
    price_per_kwh: 0.092042
  - start_time: "2026-04-02T00:00:00+00:00"
    end_time: "2026-04-02T01:00:00+00:00"
    price_per_kwh: 0.090058
  - start_time: "2026-04-02T01:00:00+00:00"
    end_time: "2026-04-02T02:00:00+00:00"
    price_per_kwh: 0.126067
```

### 3. Average Market Price Sensor

The sensor value reports the average ELEX market price during the day. The sensor value reports the market price in €/kWh.

### 4. Median Market Price Sensor

The sensor value reports the median ELEX market price during the day. The sensor value reports the market price in €/kWh.

### 5. Lowest Market Price Sensor

The sensor value reports the lowest ELEX market price during the day. The sensor value reports the market price in €/kWh. The market price in €/kWh is available as a sensor attribute.

The sensor attributes contain the start and end time of the lowest market price timeframe.

```yaml
market_price_per_kwh: 0.09
start_time: "2026-04-01T22:00:00+00:00"
end_time: "2026-04-01T23:00:00+00:00"
```

### 6. Highest Market Price Sensor

The sensor value reports the highest ELEX market price during the day. The sensor value reports the market price in €/kWh. The market price in €/kWh is available as a sensor attribute.

The sensor attributes contain the start and end time of the highest market price timeframe.

```yaml
price_per_kwh: 0.33
start_time: "2026-04-01T18:00:00+00:00"
end_time: "2026-04-01T19:00:00+00:00"
```

### 7. Quantile Sensor

The sensor value reports the quantile between the lowest market price and the highest market price during the day in the range between 0 & 1.

Examples:

- The sensor reports 0 if the current market price is the lowest during the day.
- The sensor reports 1 if the current market price is the highest during the day.
- If the sensor reports e.g., 0.25, then the current market price is 25% of the range between the lowest and the highest market price.

### 8. Rank Sensor

The sensor value reports the rank of the current market price during the day. Or in other words: The number of hours in which the price is lower than the current price.

Examples:

- The sensor reports 0 if the current market price is the lowest during the day. There is no lower market price during the day.
- The sensor reports 23 if the current market price is the highest during the day (if the market price will be updated hourly). There are 23 hours which are cheaper than the current hour market price.
- The sensor reports 1 if the current market price is the 2nd cheapest during the day. There is 1 hour which is cheaper than the current hour market price.

## Service Calls

List of Service Calls:

- Get Lowest Price Interval
- Get Highest Price Interval
- Fetch Data

### 1. Get Lowest and Highest Price Interval

Get the time interval during which the price is at its lowest/highest point.

Knowing the hours with the lowest / highest consecutive prices during the day could be an interesting use case. This might be of value when looking for the most optimum time to start your washing machine, dishwasher, dryer, etc.

With this service call, you can let the integration calculate the optimal start time. The only mandatory attribute is the duration of your appliance. Optionally you can limit start- and end-time, e.g. to start your appliance only during night hours.

```yaml
elex.get_lowest_price_interval
elex.get_highest_price_interval
```

| Service data attribute | Optional | Description                                                                 | Example                          |
| ---------------------- | -------- | --------------------------------------------------------------------------- | -------------------------------- |
| `device_id`            | yes      | An ELEX service instance ID. In case you have multiple ELEX instances.      | 9d44d8ce9b19e0863cf574c2763749ac |
| `earliest_start`       | yes      | Earliest time to start the appliance.                                       | "14:00:00"                       |
| `earliest_start_post`  | yes      | Postponement of `earliest_start` in days: 0 = today (default), 1 = tomorrow | 0                                |
| `latest_end`           | yes      | Latest time to end the appliance.                                           | "16:00:00"                       |
| `latest_end_post`      | yes      | Postponement of `latest_end` in days: 0 = today (default), 1 = tomorrow     | 0                                |
| `duration`             | no       | Required duration to complete appliance.                                    | See below...                     |

Notes:

- If `earliest_start` is omitted, the current time is used instead.
- If `latest_end` is omitted, the end of all available market data is used.
- `earliest_start` refers to today if `earliest_start_post` is omitted or set to 0.
- `latest_end` will be automatically trimmed to the available market area.
- If `earliest_start` and `latest_end` are present _and_ `latest_end` is earlier than (or equal to) `earliest_start`, then `latest_end` refers to tomorrow.
- `device_id` is only required if you have setup multiple ELEX instances. The easiest way to get the unique device id is to use the _Developer Tools -> Services_.

Service Call Examples:

```yaml
action: elex.get_lowest_price_interval
data:
  device_id: 9d44d8ce9b19e0863cf574c2763749ac
  earliest_start: "14:00:00"
  latest_end: "16:00:00"
  duration:
    hours: 1
    minutes: 0
    seconds: 0
```

```yaml
action: elex.get_lowest_price_interval
data:
  earliest_start: "14:00:00"
  latest_end: "16:00:00"
  duration: "00:30:00" # 30 minutes
```

```yaml
action: elex.get_lowest_price_interval
data:
  duration: "00:30" # 30 minutes
```

```yaml
# get the lowest price all day tomorrow:
action: elex.get_lowest_price_interval
data:
  earliest_start: "00:00:00"
  earliest_start_post: 1
  latest_end: "00:00:00"
  latest_end_post: 2
  duration: "01:30:00" # 1h, 30 minutes
```

#### Response

The response contains the calculated start and end-time and the average price per kWh.

Example:

```yaml
start: "2026-04-01T23:00:00+01:00"
end: "2026-04-02T00:00:00+01:00"
market_price_per_kwh: 0.098192
total_price_per_kwh: 0.13223
```

You can use the [Template Integration](https://www.home-assistant.io/integrations/template/) to create a sensor (in your `configuration.yaml` file) that shows the start time:

![Start Appliance Sensor](/images/start_appliance_sensor.png)

```yaml
template:
  - triggers:
      - trigger: time
        at: "00:00:00"
    actions:
      - action: elex.get_lowest_price_interval
        data:
          earliest_start: "20:00:00"
          latest_end: "23:00:00"
          duration:
            hours: 1
            minutes: 5
        response_variable: resp
    sensor:
      - name: Start Appliance
        device_class: timestamp
        state: "{{ resp.start is defined and resp.start }}"
```

This sensor can be used to trigger automations:

```yaml
triggers:
  - trigger: time
    at: sensor.start_appliance
conditions: []
actions: []
```

### 2. Fetch Data

Fetch data manually from the ELEX API.

```yaml
elex.fetch_data
```

| Service data attribute | Optional | Description                                                                 | Example                          |
| ---------------------- | -------- | --------------------------------------------------------------------------- | -------------------------------- |
| `device_id`            | yes      | An ELEX service instance ID. In case you have multiple ELEX instances.      | 9d44d8ce9b19e0863cf574c2763749ac |

## FAQ

### 1. How can I show a chart of the next hours?

With [ApexCharts](https://github.com/RomRider/apexcharts-card), you can easily show a chart like this to see the hourly market prices for today:

![apexchart](/images/apexcharts.png)

You just have to install [ApexCharts](https://github.com/RomRider/apexcharts-card) (via HACS) and enter the following data in the card configuration:

```yaml
type: custom:apexcharts-card
header:
  show: true
  title: ELEX Spot Prices
  show_states: true
  colorize_states: true
graph_span: 48h
span:
  start: day
now:
  show: true
  label: Now
series:
  - entity: sensor.elex_data_total_price
    name: Electricity Price
    type: column
    float_precision: 3
    extend_to: end
    data_generator: |
      return entity.attributes.data.map((entry) => {
        return [new Date(entry.start_time).getTime(), entry.price_per_kwh];
      });
yaxis:
  - decimals: 3
```

**Assumptions:**
If your data source does not report prices for the next day, you can change the `graph_span` to `24h` to get rid of the empty space that this configuration would create.

### 2. How can I optimise the best moment to start appliances?

It might be an interesting use case to know what the hours with lowest consecutive prices during the day are. This might be of value when looking for the most optimum time to start your washing machine, dishwasher, dryer, etc. 

#### Example 1: Manually starting / scheduling a "dumb" dishwasher

- Your dishwasher cycle takes 3 hours and 15 minutes to run
- You want to run a full, continuous cycle in the time-window when power is the cheapest for those 3 hours & 15 minutes
- You don't care at what exact time the dishwasher cycle starts or finishes

Depending on your implementation use-case, there are two ways to proceed:

**Case 1: Automating the dishwasher with a smart-plug**
If the dishwasher resumes its wash cycle after a power loss, you can use a smart-plug to cut power to the dishwasher as soon as it starts and then restore power to it when your cheapest window time hits.

**Case 2: Manually starting / scheduling the dishwasher**
If you don't have a smart-plug or if your dishwasher won't resume after a power loss, you can create a card on your dashboard that tells you either what time, or in how much time you should manually start your dishwasher or schedule it to start.

_What time should I start the dishwasher?_
Create a Template Sensor under Settings → Devices & Services → Helpers → Create Helper → Template → Template a sensor.

```yaml
{% set data = state_attr('binary_sensor.dishwasher_cheapest_window', 'data') %}
{% set now = now() %}
{% set future_windows = data | selectattr('start_time', '>', now.timestamp() | timestamp_local) | list %}
{% if future_windows %}
  {% set next_window = future_windows | first %}
  {% set start_time = strptime(next_window['start_time'], '%Y-%m-%dT%H:%M:%S%z') %}
  {{ start_time.strftime('%H:%M on %d/%m/%y') }}
{% else %}
  Waiting for new data
{% endif %}
```

_In how much time from now should I start the dishwasher?_

```yaml
{% set data = state_attr('binary_sensor.dishwasher_cheapest_window', 'data') %}
{% set now = now() %}
{% set future_windows = data | selectattr('start_time', '>', now.timestamp() | timestamp_local) | list %}
{% if future_windows %}
  {% set next_window = future_windows | first %}
  {% set start_time = strptime(next_window['start_time'], '%Y-%m-%dT%H:%M:%S%z') %}
  {% set time_to_start = (start_time - now).total_seconds() %}
  {% set hours = (time_to_start // 3600) | int %}
  {% set minutes = ((time_to_start % 3600) // 60) | int %}
  {% set time_str = '{:02}:{:02}'.format(hours, minutes) %}
  {{ time_str }}
{% else %}
  Waiting for new data
{% endif %}
```

#### Example 2: Automating a Home-Assistant-Connected Washer/Dryer

- The appliance reports how long each cycle takes to Home Assistant
- The appliance can be remote-controlled via Home Assistant
- You want to run a full, continuous cycle in the time-window when power is the cheapest.

Here's what such an automation may look like:

```yaml
mode: single
triggers:
  - trigger: state
    entity_id:
      - sensor.aeg_washer_dryer_appliancestate
    from: Ready To Start
    to: Running
conditions: []
actions:
  - action: button.press
    target:
      entity_id: button.aeg_washer_dryer_executecommand_pause
  - data:
      duration:
        hours: 0
        minutes: "{{ states('sensor.aeg_washer_dryer_timetoend') | int }}"
        seconds: 0
    response_variable: cheapest_window
    action: elex.get_lowest_price_interval
  - wait_template: >-
      {{ cheapest_window is defined and as_timestamp(cheapest_window.start) | int > 0 }}
    continue_on_timeout: true
  - delay:
      seconds: >
        {% set wait = as_timestamp(cheapest_window.start) - as_timestamp(now()) %}
        {{ [wait, 0] | max | int }}
  - action: button.press
    target:
      entity_id: button.aeg_washer_dryer_executecommand_resume
```

### 3. I want to combine and view everything

Here's another [ApexCharts](https://github.com/RomRider/apexcharts-card) example.
It shows the price for the current day, the next day and the `min/max` value for each day.
Furthermore, it also fills the hours during which prices are lowest (see 2.)

![apexchart](/images/apex_advanced.png)

```yaml
type: custom:apexcharts-card
header:
  show: true
  title: ELEX Market Prices
graph_span: 48h
span:
  start: day
now:
  show: true
  label: Now
series:
  - entity: sensor.elex_data_market_price
    name: €/kWh
    type: line
    curve: stepline
    float_precision: 3
    extend_to: end
    show:
      extremas: true
    # This automatically groups your 15-min data into clean 1-hour steps on the chart
    group_by:
      func: avg
      duration: 1h
    data_generator: >
      return entity.attributes.data.map((entry) => {
        return [new Date(entry.start_time).getTime(), entry.price_per_kwh];
      });
    color_threshold:
      - value: 0
        color: "#186ddc"
      - value: 0.100
        color: "#04822e"
      - value: 0.150
        color: "#12A141"
      - value: 0.200
        color: "#F3DC0C"
      - value: 0.250
        color: red
      - value: 0.350
        color: magenta
experimental:
  color_threshold: true
yaxis:
  - decimals: 3
    apex_config:
      title:
        text: €/kWh
      tickAmount: 5
apex_config:
  stroke:
    width: 2
  legend:
    show: false
  tooltip:
    x:
      show: true
      format: "dd MMM, HH:mm"
```