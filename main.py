from app import app
from api import api
from filler_db_openweather_data.filler import fill_db

if __name__ == '__main__':
    cities = [
        ('Kyiv', 50.433, 30.5167),
        ('Lviv', 49.8383, 24.0232),
        ('Kharkiv', 50.00, 36.25),
        ('Odesa', 46.4775, 30.7326),
        ('Dnipro', 48.45, 34.9833),
    ]

    # fill_db(cities)

    app.run()
