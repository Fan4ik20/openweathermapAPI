from typing import List

from weather_db.db_manager import City, WeatherForecast

from openweathermap.weather_parser import OpenWeatherMapParser
from support_functions.converters import (
    convert_openweather_data_to_desired_format
)

from secrets_ import openweathermap_key


def send_requests_for_cities(cities: List[tuple]) -> List[dict]:
    """For every city sends request to openweather API.
    All received data are placed in a list that will be returned.

    """

    parser = OpenWeatherMapParser(openweathermap_key)

    received_data = []

    for name, lat, lon in cities:
        received_data.append(
            parser.get_daily_one_call_request_data((lat, lon))
        )

    return received_data


def _create_weather_data_to_insert(converted_data: dict) -> list:
    data_to_insert = []

    for daily_data in converted_data['daily']:
        city = converted_data['city']

        data_to_insert.append(
            (City.get_city_id_by_name(city), *daily_data.values())
        )

    return data_to_insert


def fill_db(cities: List[tuple]) -> None:
    """Function for filling the database. Depending on the specified cities,
    it sends requests to the openweathermap API,
    converts the raw data into a single format
    and inserts the data into the database.

    """

    City.insert_cities(cities)

    received_weather_list = send_requests_for_cities(cities)

    weather_list_length = len(received_weather_list)
    for index, weather_data in enumerate(received_weather_list):
        print(f'Processing the {index + 1} requests of {weather_list_length}')

        converted_data = convert_openweather_data_to_desired_format(
            weather_data
        )
        weather_data_to_insert = _create_weather_data_to_insert(converted_data)

        WeatherForecast.insert_weather_forecasts(weather_data_to_insert)
