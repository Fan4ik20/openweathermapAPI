# OpenWeatherMapApi
## Overview
This program contains two main parts:
- OpenWeatherMap data parser (gives a forecast for today and 7 days ahead)  
You can find it at openweathermap package
- API that represents parsed data (api docs you can find on `/apidocs/` endpoint)

## Requirements
All necessary requirements is specified in the requirements.txt file

## Installation
- Install all python modules via command `pip install -r requirements.txt`

## Running
- At the first launch you will need to fill in the database (or you can use an existing).  
To do this you can use `fill_weather_db` function from `filler_db_openweather_data.filler` module  
To use the function it is necessary to provide the variable env openweathermap_key  
or pass the api key directly to the fill_weather_db function.  
Function accept a List of tuples. Tuple format - (city_name, lat, lon)
- Simple run main.py script from the root directory

## Additional
How the api works, with beautiful output,  
you can see by running the module `request_samples.py`.
