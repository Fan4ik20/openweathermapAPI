"""In this module you will find the
basic functions for CRUD operations with the db.

"""
import sqlite3
from contextlib import contextmanager
from typing import List, Union

from app import db_name as weather_db


@contextmanager
def _db_connect(db_name) -> None:
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    yield cur

    conn.commit()
    conn.close()


class WeatherDb:
    @staticmethod
    def create_city_table() -> None:
        with _db_connect(weather_db) as cur:
            cur.execute(
                '''CREATE TABLE IF NOT EXISTS City
                (
                    city_id INTEGER PRIMARY KEY,
                    "name" VARCHAR(255) NOT NULL,
                    latitude FLOAT,
                    longitude FLOAT
                );
                '''
            )

    @staticmethod
    def create_weather_table() -> None:
        with _db_connect(weather_db) as cur:
            cur.execute(
                '''CREATE TABLE IF NOT EXISTS WeatherForecast
                    (
                        forecast_id INTEGER PRIMARY KEY,
                        date TEXT NOT NULL,
                        temp FLOAT NOT NULL,
                        pcp FLOAT,
                        clouds INT NOT NULL,
                        pressure INT NOT NULL,
                        humidity TINYINT NOT NULL,
                        wind_speed FLOAT NOT NULL,
                    
                        city_id INTEGER NOT NULL,
                        
                        CONSTRAINT fk_forecast_city FOREIGN KEY (city_id)
                        REFERENCES City(city_id)
                     );
                '''
            )

    @classmethod
    def create_tables(cls) -> None:
        cls.create_city_table()
        cls.create_weather_table()

    @staticmethod
    def _drop_table(table_name: str) -> None:
        with _db_connect(weather_db) as cur:
            cur.execute(f"DROP TABLE {table_name}")

    @classmethod
    def drop_city_table(cls) -> None:
        cls._drop_table('City')

    @classmethod
    def drop_weather_forecast_table(cls) -> None:
        cls._drop_table('WeatherForecast')

    @classmethod
    def drop_tables(cls) -> None:
        cls.drop_city_table()
        cls.drop_weather_forecast_table()


class City:
    _sql_for_insert = (
        '''INSERT INTO City("name", latitude, longitude) VALUES (
            ?, ?, ?
          );
          '''
    )

    @classmethod
    def insert_city(cls, name: str, coordinates: tuple) -> None:
        lat, lon = coordinates

        with _db_connect(weather_db) as cur:
            cur.execute(cls._sql_for_insert, (name, lat, lon))

    @classmethod
    def insert_cities(cls, cities_data: List[tuple]) -> None:
        with _db_connect(weather_db) as cur:
            cur.executemany(cls._sql_for_insert, cities_data)

    @staticmethod
    def get_all_cities() -> List[tuple]:
        with _db_connect(weather_db) as cur:
            cur.execute(
                'SELECT city_id, "name", latitude, longitude FROM City;'
            )
            cities = cur.fetchall()

        return cities

    @staticmethod
    def get_city_id_by_name(name: str) -> Union[int, None]:
        with _db_connect(weather_db) as cur:
            cur.execute(
                'SELECT city_id FROM City WHERE name=?;', (name,)
            )
            city_id = cur.fetchone()

        return city_id[0] if city_id else None

    @staticmethod
    def get_city_data_by_id(city_id: int) -> tuple:
        with _db_connect(weather_db) as cur:
            cur.execute(
                'SELECT city_id, "name", latitude, longitude FROM City'
                'WHERE city_id=?;', (city_id,)
            )
            city = cur.fetchone()

        return city


class WeatherForecast:
    _sql_for_insert = (
        '''INSERT INTO WeatherForecast(
            city_id, "date", temp, pcp, clouds, pressure, humidity, wind_speed
        ) VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?
        );'''
    )

    @classmethod
    def insert_weather_forecast(
            cls,  city_name: str, date: str, temp: float, pcp: float,
            clouds: int, pressure: int, humidity: int, wind_speed: float
    ) -> None:
        city_id = City.get_city_id_by_name(city_name)

        with _db_connect(weather_db) as cur:
            cur.execute(
                cls._sql_for_insert,
                (
                    city_id, date, temp, pcp, clouds,
                    pressure, humidity, wind_speed
                )
            )

    @classmethod
    def insert_weather_forecasts(
            cls, weather_forecasts_data: List[tuple]
    ) -> None:

        with _db_connect(weather_db) as cur:
            cur.executemany(cls._sql_for_insert, weather_forecasts_data)

    @staticmethod
    def select_all_weather_forecasts() -> List[tuple]:
        with _db_connect(weather_db) as cur:
            cur.execute(
                '''SELECT forecast_id, "date", temp, pcp, clouds, 
                    pressure, humidity, wind_speed, city_id 
                    FROM WeatherForecast; 
                '''
            )

            weather_forecasts = cur.fetchall()

        return weather_forecasts
