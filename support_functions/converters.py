from datetime import datetime
from statistics import mean

from geopy.geocoders import Nominatim


def get_city_name_from_coords(coords: tuple) -> str:
    geolocator = Nominatim(user_agent='my_app')

    return geolocator.reverse(
        coords, language='en', exactly_one=True
    ).raw['address']['city']


def convert_unix_time_to_date(unix_time: int) -> str:
    return datetime.fromtimestamp(unix_time).strftime(
        '%Y-%m-%d'
    )


def _convert_daily_data(daily_data: list) -> list:
    daily_list = []

    for data in daily_data:
        daily_list.append({
            'date': convert_unix_time_to_date(data['dt']),
            'temp': mean(
                [data['temp']['day'], data['temp']['night'],
                 data['temp']['eve'], data['temp']['morn']]
            ),
            'pcp': data.get('rain'),
            'clouds': data['clouds'],
            'pressure': data['pressure'],
            'humidity': data['humidity'],
            'wind_speed': data['wind_speed']
        })

    return daily_list


def convert_openweather_data_to_desired_format(openweather_data: dict) -> dict:
    coordinates = openweather_data['lat'], openweather_data['lon']
    city = get_city_name_from_coords(coordinates)

    data_in_desired_format = {
        'city': city,
        'daily': _convert_daily_data(openweather_data['daily'])
    }

    return data_in_desired_format
