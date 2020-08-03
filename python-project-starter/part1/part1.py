import json
from datetime import datetime

DEGREE_SYMBOL = u"\N{DEGREE SIGN}C"

def format_temperature(temp):
    """Takes a temperature and returns it in string format with the degrees and celsius symbols.
    
    Args:
        temp: A string representing a temperature.
    Returns:
        A string contain the temperature and "degrees celcius."
    """
    return f"{temp}{DEGREE_SYMBOL}"

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


def calculate_mean(total, num_items):
    """Calculates the mean.
    
    Args:
        total: integer representing the sum of the numbers.
        num_items: integer representing the number of items counted.
    Returns:
        An integer representing the mean of the numbers.
    """
    mean = round(total / num_items, 1)
    return mean

def find_averages(loaded_forecast_data):
    """ Analyse data to find averages for five day overview 
    
    Args:
        loaded_forecast_file: A list of data created from imported JSON file
        
    Returns:
        A series of print statements with lowest temperature, highest tempereature, average low
        and average high 
    """

    min_temps = {}
    max_temps = {}
    
    for i in range(len(loaded_forecast_data)):
        min_temp = convert_f_to_c(loaded_forecast_data[i]["Temperature"]["Minimum"]["Value"])
        min_temps[convert_date(loaded_forecast_data[i]["Date"])] = min_temp
        max_temp = convert_f_to_c(loaded_forecast_data[i]["Temperature"]["Maximum"]["Value"])
        max_temps[convert_date(loaded_forecast_data[i]["Date"])] = max_temp


    lowest_temp = min(temp for day, temp in min_temps.items())

    lowest_temp_day = [day for (day, temp) in min_temps.items() if temp == lowest_temp]
    lowest_temp_day = str(lowest_temp_day[0])
    
    highest_temp = max(temp for day, temp in max_temps.items())

    highest_temp_day = [day for (day, temp) in max_temps.items() if temp == highest_temp]
    highest_temp_day = str(highest_temp_day[0])

    sum_min_temps = 0
    for day, temp in min_temps.items():
        sum_min_temps += temp
    
    avg_low = calculate_mean(sum_min_temps, len(min_temps))

    sum_max_temps = 0
    for day, temp in max_temps.items():
        sum_max_temps += temp
    
    avg_high = calculate_mean(sum_max_temps, len(max_temps))
    no_days = len(loaded_forecast_data)

    # print(f"{no_days} Day Overview")
    # print(f"    The lowest temperature will be {lowest_temp}°C, and will occur on {lowest_temp_day}.")
    # print(f"    The highest temperature will be {highest_temp}°C, and will occur on {highest_temp_day}.")
    # print(f"    The average low this week is {avg_low}°C.")
    # print(f"    The average high this week is {avg_high}°C.")
    # print()

    overview = f"{no_days} Day Overview\n    The lowest temperature will be {lowest_temp}°C, and will occur on {lowest_temp_day}.\n    The highest temperature will be {highest_temp}°C, and will occur on {highest_temp_day}.\n    The average low this week is {avg_low}°C.\n    The average high this week is {avg_high}°C.\n\n"

    return overview

def process_weather(forecast_file):
    """Converts raw weather data into meaningful text.

    Args:
        forecast_file: A string representing the file path to a file
            containing raw weather data.
    Returns:
        A string containing the processed and formatted weather data.
    """

    with open(forecast_file) as json_file:
        json_data = json.load(json_file)

    daily_forecasts = json_data["DailyForecasts"] # daily_forecasts is a LIST of DICTIONARIES
    # print(daily_forecasts[0]) # type = DICT
    
    find_averages(daily_forecasts)
    final_output = ""

    for i in range(len(daily_forecasts)):

        # DATE
        converted_date = convert_date(daily_forecasts[i]["Date"])
        # print(f"-------- {converted_date} --------")

        # TEMPERATURES
        if daily_forecasts[i]["Temperature"]["Minimum"]["Unit"] == "F":
            min_temp = convert_f_to_c(daily_forecasts[i]["Temperature"]["Minimum"]["Value"])
        else:
            min_temp = daily_forecasts[i]["Temperature"]["Minimum"]["Value"]
        # print(f"Minimum Temperature: {min_temp}°C")
        if daily_forecasts[i]["Temperature"]["Maximum"]["Unit"] == "F":
            max_temp = convert_f_to_c(daily_forecasts[i]["Temperature"]["Maximum"]["Value"])
        else:
            min_temp = daily_forecasts[i]["Temperature"]["Maximum"]["Value"]
        # print(f"Maximum Temperature: {max_temp}°C")

        # DAYTIME
        day_description = daily_forecasts[i]["Day"]["LongPhrase"]
        # print(f"Daytime: {day_description}")

        day_rain_prob = daily_forecasts[i]["Day"]["RainProbability"]
        # print(f"    Chance of rain: {rain_prob}%")

        # NIGHTTIME
        night_description = daily_forecasts[i]["Night"]["LongPhrase"]
        # print(f"Nighttime: {night_description}")

        night_rain_prob = daily_forecasts[i]["Night"]["RainProbability"]
        # print(f"    Chance of rain: {rain_prob}%")
        
        # print()

        processed_weather = f"-------- {converted_date} --------\nMinimum Temperature: {min_temp}°C\nMaximum Temperature: {max_temp}°C\nDaytime: {day_description}\n    Chance of rain: {day_rain_prob}%\nNighttime: {night_description}\n    Chance of rain: {night_rain_prob}%\n\n"

        final_output = final_output + processed_weather

    overview = find_averages(daily_forecasts)
    final_output = overview + final_output
    # final_output = final_output[:-2]

    return final_output

    


if __name__ == "__main__":
    a = process_weather("data/forecast_5days_a.json")
    print(a)
    # print(process_weather("data/forecast_8days.json"))

# lines = a.split('\n')
# # lines = [line for line in lines if line.strip()]
# for line in lines:
#     print(line)

# print(lines)

# filepath = "data/forecast_5days_a.json"
# filepath = "data/forecast_5days_b.json"
# filepath = "data/forecast_8days.json"
# forecast = process_weather(filepath)
