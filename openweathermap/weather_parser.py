"""This module contains class
for sending requests to the openweathermap API.

"""
import json

import requests


class OpenWeatherMapParser:
    def __init__(self, weather_api_key):
        self._api_key = weather_api_key

    def _send_daily_one_call_request(self, coords: tuple) -> dict:
        """Sends a request to the onecall API openweathermap endpoint."""

        lat, lon = coords

        data = requests.get(
            'https://api.openweathermap.org/data/2.5/'
            f'onecall?lat={lat}&lon={lon}&exclude=current,minutely,hourly'
            '&units=metric'
            f'&appid={self._api_key}&lang=ua'
        ).json()

        return data

    def get_daily_one_call_request_data(self, coords: tuple) -> dict:
        return self._send_daily_one_call_request(coords)

    @staticmethod
    def write_json_data(data: dict, filepath: str) -> None:
        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)

    def get_and_write_daily_one_call_requests_data(
            self, coords: tuple, filepath: str
    ) -> dict:

        data = self._send_daily_one_call_request(coords)

        self.write_json_data(data, filepath)

        return data

    @staticmethod
    def read_json_data_from_file(filepath: str) -> dict:
        with open(filepath, encoding='utf-8') as file:
            return json.load(file)
