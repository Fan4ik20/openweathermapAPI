import requests


class APIRequests:
    def __init__(self, domain: str):
        self._domain = domain

    @staticmethod
    def _print_wrong_request(wrong_request_data: dict):
        print('-' * 5, 'Wrong Request', '-' * 5)

        print(f'Error message is "{wrong_request_data["msg"]}"')

    @staticmethod
    def _print_formatted_cities_request(cities_data: dict) -> None:
        for city_data in cities_data['cities']:
            city_id, city_name, city_coords = city_data.values()
            lat, lon = city_coords.values()

            print(f'City id: {city_id}, City name: {city_name}, '
                  f'latitude: {lat}, longitude: {lon}')
            print('-' * 10)

    def print_cities_request(self) -> None:
        print('-' * 5, '/api/v1/cities/', '-' * 5)
        self._print_formatted_cities_request(
            requests.get(f'{self._domain}/api/v1/cities/').json()
        )

    @staticmethod
    def _print_formatted_mean_request(mean_data: dict) -> None:
        city, mean_value = mean_data.values()
        value_type, value = mean_value.values()

        print('-' * 5, 'Right Request', '-' * 5)
        print(f'The average {value_type} in {city} is {value:.2f}')

    def print_mean_requests(self) -> None:
        print('-' * 5, '/api/v1/mean/', '-' * 5)
        self._print_formatted_mean_request(
            requests.get(
                f'{self._domain}/api/v1/mean/?city=Kyiv&value_type=pcp'
            ).json()
        )

        self._print_wrong_request(
            requests.get(
                f'{self._domain}/api/v1/mean/?city=Kharkiv'
            ).json()
        )

    @staticmethod
    def _print_formatted_records_request(records_data: dict) -> None:
        print('-' * 5, 'Right Request', '-' * 5)
        city, start_dt, end_dt, daily_forecast = records_data.values()

        print(f'The weather forecast in {city} '
              f'for the days {start_dt} to {end_dt}:')

        for weather_forecast in daily_forecast:
            (forecast_id, date, temp, pcp, clouds,
             pressure, humidity, wind_speed) = weather_forecast.values()

            print(f'For the day {date}, the forecast is:\n'
                  f'temperature - {temp:.2f}, '
                  f'daily rainfall - {pcp if pcp else 0: .2f}, '
                  f'cloudy - {clouds}, pressure - {pressure},'
                  f'humidity - {humidity}, wind speed - {wind_speed}')
            print('-' * 10)

    def print_records_request(self) -> None:
        print('-' * 5, '/api/v1/records/', '-' * 5)

        self._print_formatted_records_request(
            requests.get(
                f'{self._domain}/api/v1/records/'
                '?city=Odesa&start_dt=2021-12-16&end_dt=2021-12-20'
            ).json()
        )

        self._print_wrong_request(
            requests.get(
                f'{self._domain}/api/v1/records/'
                '?start_dt=2021-12-15&end_dt=2021-12-21'
            ).json()
        )

    @staticmethod
    def _print_formatted_moving_mean_request(moving_mean_data: dict) -> None:
        print('-' * 5, 'Right Request', '-' * 5)

        city, n, moving_average = moving_mean_data.values()
        value_type, values = moving_average.values()

        print(f'In the city of {city}, '
              f'the moving average with a coefficient of {n} '
              f'is - ({", ".join(map(str, values))})')

    def print_moving_mean_requests(self) -> None:
        print('-' * 5, '/api/v1/moving_mean/', '-' * 5)

        self._print_formatted_moving_mean_request(
            requests.get(
                f'{self._domain}/api/v1/moving_mean/'
                '?city=Dnipro&value_type=humidity&n=4'
            ).json()
        )

        self._print_wrong_request(
            requests.get(
                f'{self._domain}/api/v1/moving_mean/'
                '?city=Kyiv&value_type=wind_speed&n=25'
            ).json()
        )


def main():
    requester = APIRequests('http://127.0.0.1:5000')

    requester.print_cities_request()
    print('\n', '-' * 10, '\n')
    requester.print_mean_requests()
    print('\n', '-' * 10, '\n')
    requester.print_records_request()
    print('\n', '-' * 10, '\n')
    requester.print_moving_mean_requests()
    print('\n', '-' * 10, '\n')


if __name__ == '__main__':
    main()
