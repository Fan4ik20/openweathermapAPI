from typing import List

from flask import request
from flask_restful import Api, Resource, abort
from flasgger import Swagger, swag_from

from app import app
from api.schemas import MeanSchema, RecordsSchema, MovingAverageSchema

from support_functions.calculators import calculate_moving_average

from weather_db.db_manager import City, WeatherForecast


api = Api(app)
swagger = Swagger(app)

mean_schema = MeanSchema()
records_schema = RecordsSchema()
moving_average_schema = MovingAverageSchema()


class CitiesApi(Resource):
    @staticmethod
    def build_json_response(cities: List[tuple]) -> dict:
        cities_list = []

        for city_id, name, lat, lon in cities:
            cities_list.append({
                'id': city_id,
                'name': name,
                'coords': {'lat': lat, 'lon': lon}
            })

        return {'cities': cities_list}

    @classmethod
    @swag_from('yml_for_swagger/cities_swagger.yml')
    def get(cls) -> dict:
        cities = City.get_all_cities()

        if not cities:
            abort(404, msg='There is no available cities.')

        return cls.build_json_response(cities)


class MeanApi(Resource):
    @staticmethod
    def build_json_response(
            city: str, value_type: str, mean_value: float
    ) -> dict:

        return {
            'city': city,
            'mean_value': {
                'value_type': value_type,
                'value': mean_value
            }
        }

    @classmethod
    @swag_from('yml_for_swagger/mean_swagger.yml')
    def get(cls) -> dict:
        errors = mean_schema.validate(request.args)

        if errors:
            abort(404, msg=str(errors))

        city, value_type = request.args['city'], request.args['value_type']

        mean_value = None
        try:
            mean_value = WeatherForecast.select_mean_value_of_column(
                city, value_type
            )
        except ValueError as error:
            abort(404, msg=str(error))

        return cls.build_json_response(city, value_type, mean_value)


class RecordsApi(Resource):
    @staticmethod
    def build_json_response(
            city: str, start_dt: str, end_dt: str,
            weather_forecast_data: List[tuple]
    ) -> dict:

        daily_weather_forecast = []

        for weather_forecast in weather_forecast_data:
            (
                forecast_id, date, temp,
                pcp, clouds, pressure, humidity, wind_speed
            ) = weather_forecast

            daily_weather_forecast.append(
                {
                    'id': forecast_id,
                    'date': date,
                    'temp': temp,
                    'pcp': pcp,
                    'clouds': clouds,
                    'pressure': pressure,
                    'humidity': humidity,
                    'wind_speed': wind_speed
                }
            )

        return {
            'city': city, 'start_dt': start_dt, 'end_dt': end_dt,
            'daily_forecast': daily_weather_forecast
        }

    @classmethod
    @swag_from('yml_for_swagger/records_swagger.yml')
    def get(cls) -> dict:
        errors = records_schema.validate(request.args)

        if errors:
            abort(404, msg=str(errors))

        args = request.args
        city, start_dt, end_dt = args['city'], args['start_dt'], args['end_dt']

        forecast_records = WeatherForecast.select_records_in_given_range(
            city, start_dt, end_dt
        )

        return cls.build_json_response(
            city, start_dt, end_dt, forecast_records
        )


class MovingAverageApi(Resource):
    @staticmethod
    def build_json_response(
            city: str, value_type: str, n: str, moving_average: list
    ) -> dict:

        return {
            'city': city,
            'n': n,
            'moving_average': {
                'value_type': value_type,
                'values': moving_average
            }
        }

    @classmethod
    @swag_from('yml_for_swagger/moving_average_swagger.yml')
    def get(cls) -> dict:
        errors = moving_average_schema.validate(request.args)

        if errors:
            abort(404, msg=str(errors))

        args = request.args
        city, value_type, n = args['city'], args['value_type'], args['n']

        column_values = WeatherForecast.select_records_of_given_column(
            city, value_type
        )

        moving_average = None
        try:
            moving_average = calculate_moving_average(
                [value[0] if value[0] else 0 for value in column_values],
                int(n)
            )
        except ValueError as error:
            abort(404, msg=str(error))

        return cls.build_json_response(city, value_type, n, moving_average)


api.add_resource(CitiesApi, '/api/v1/cities/')
api.add_resource(MeanApi, '/api/v1/mean/')
api.add_resource(RecordsApi, '/api/v1/records/')
api.add_resource(MovingAverageApi, '/api/v1/moving_mean/')
