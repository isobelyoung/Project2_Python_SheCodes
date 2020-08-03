import json
import plotly.express as px
from datetime import datetime
import numpy as np

def convert_date(iso_string):
    """Converts and ISO formatted date into a human readable format.
    
    Args:
        iso_string: An ISO date string..
    Returns:
        A date formatted like: Weekday Date Month Year
    """
    d = datetime.strptime(iso_string, "%Y-%m-%dT%H:%M:%S%z")
    return d.strftime("%A %d %B %Y")


def convert_f_to_c(temp_in_farenheit):
    """Converts an temperature from farenheit to celsius

    Args:
        temp_in_farenheit: integer representing a temperature.
    Returns:
        An integer representing a temperature in degrees celsius.
    """
    temp_in_celsius = float((temp_in_farenheit - 32) * 5 / 9)
    return round(temp_in_celsius, 1)

forecast_file = "data/forecast_8days.json"
with open(forecast_file) as json_file:
    json_data = json.load(json_file)

daily_forecasts = json_data["DailyForecasts"]
# for x in daily_forecasts:
#     for y in x.items():
#         print(y)

daily_temps = {}

# for day in daily_forecasts:
#     print(day)

for i in range(len(daily_forecasts)):
    day = convert_date(daily_forecasts[i]['Date'])
    
    min_and_max = {}
    min_and_max["Minimum"] = convert_f_to_c(daily_forecasts[i]["Temperature"]["Minimum"]["Value"])
    min_and_max["Maximum"] = convert_f_to_c(daily_forecasts[i]["Temperature"]["Maximum"]["Value"])

    daily_temps[day] = min_and_max

days = []
min_temps = []
max_temps = []

for day, temp in daily_temps.items():
    days.append(day)
    min_temps.append(temp["Minimum"])
    max_temps.append(temp["Maximum"])

# print(days)
# print(min_temps)
# print(max_temps)

df = {
    "Minimum Temperature": min_temps,
    "Maximum Temperature": max_temps,
    "days": days
}

fig = px.line(
    df,
    y=["Minimum Temperature", "Maximum Temperature"], #specify two values for y, 
    x="days"
)

fig.update_layout(
    title="Daily Forecast: Minimum and Maximum Temperatures",
    xaxis_title="Day",
    yaxis_title="Temperature (°C)",
    legend_title="Key:",
    font=dict(
        family="Courier New, monospace",
        size=14,
        color="#373737"
    )
)


fig.show()

daily_realfeel = {}

for i in range(len(daily_forecasts)):
    day_realfeel = convert_date(daily_forecasts[i]['Date'])
    
    real_feel = {}
    real_feel["Minimum"] = convert_f_to_c(daily_forecasts[i]["Temperature"]["Minimum"]["Value"])
    real_feel["RealFeelTemperature"] = convert_f_to_c(daily_forecasts[i]["RealFeelTemperature"]["Minimum"]["Value"])
    real_feel["RealFeelTemperatureShade"] = convert_f_to_c(daily_forecasts[i]["RealFeelTemperatureShade"]["Minimum"]["Value"])

    daily_realfeel[day_realfeel] = real_feel

# print(daily_realfeel)

days_graph2 = []
temp_min = []
temp_realfeel = []
temp_realfeelshade = []

for day, temp in daily_realfeel.items():
    days_graph2.append(day)
    temp_min.append(temp["Minimum"])
    temp_realfeel.append(temp["RealFeelTemperature"])
    temp_realfeelshade.append(temp["RealFeelTemperatureShade"])

# print(days_graph2, temp_min, temp_realfeel, temp_realfeelshade)

df_2 = {
    "Minimum Temperature": temp_min,
    "Real Feel Temperature": temp_realfeel,
    "Real Feel Temperature Shade": temp_realfeelshade,
    "Days": days_graph2
}

fig_2 = px.bar(
    df_2,
    y=["Minimum Temperature", "Real Feel Temperature","Real Feel Temperature Shade"], #specify two values for y, 
    x="Days",
    barmode="group"
)

fig_2.update_layout(
    title="Daily Forecast: Minimum, Real Feel, and Real Feel Shade Temperatures",
    xaxis_title="Day",
    yaxis_title="Temperature (°C)",
    legend_title="Key:",
    font=dict(
        family="Courier New, monospace",
        size=14,
        color="#373737"
    )
)

# fig_2.show()