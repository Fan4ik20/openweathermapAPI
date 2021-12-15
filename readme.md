# OpenWeatherMapApi
## Overview
This program contains two main parts:
- OpenWeatherMap data parser
- API that represents parsed data (api docs you can find on `/apidocs/` endpoint)

## Requirements
All necessary requirements is specified in the requirements.txt file

## Installation
Install all python modules via command `pip install -r requirements.txt`

## Running.
- At the first launch you will need to fill in the database.  
To do this you can use `fill_db` function from `filler_db_openweather_data.filler` module  
Function accept a List of tuples. Tuple format - (city_name, lat, lon).