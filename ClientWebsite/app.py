from flask import Flask, render_template, url_for, request
import requests
from configparser import ConfigParser
import os
import time

app = Flask(__name__)

URL = "http://127.0.0.1:5000/details/"


def get_weather_key():
    config = ConfigParser()
    path = '/'.join((os.path.abspath(__file__).replace('\\', '/')).split('/')[:-1])
    config.read(os.path.join(path, 'config.ini'))
    return config['OpenWeatherMap']['main_api']


def get_elevation_key():
    config = ConfigParser()
    path = '/'.join((os.path.abspath(__file__).replace('\\', '/')).split('/')[:-1])
    config.read(os.path.join(path, 'config.ini'))
    return config['MapQuest']['main_api']


def get_elevation_data(api_key, latitude, longitude):
    url = "http://open.mapquestapi.com/elevation/v1/profile?key={}&shapeFormat=raw&latLngCollection={},{}".format(
        api_key, latitude, longitude)
    return requests.get(url).json()


def get_weather_data(api_key, location):
    url = "https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}".format(location, api_key)
    return requests.get(url).json()


def post_end_data(city):
    weather_key = get_weather_key()

    start_time_for_weather = time.time()
    weather_data = get_weather_data(weather_key, city)
    end_time_for_weather = time.time()

    time_for_weather = round(end_time_for_weather - start_time_for_weather, 7)

    elevation_key = get_elevation_key()

    longitude = weather_data['coord']['lon']
    latitude = weather_data['coord']['lat']

    start_time_for_elevation = time.time()
    elevation_data = get_elevation_data(elevation_key, latitude, longitude)
    end_time_for_elevation = time.time()

    time_for_elevation = round(end_time_for_elevation - start_time_for_elevation, 7)

    height = elevation_data['elevationProfile'][0]['height']

    weather_data['height'] = height

    # Post the response from the OpenWeather API, plus the elevation data from MapQuest to my REST API
    post_start_time = time.time()
    post = requests.post(URL, json=weather_data)
    post_end_time = time.time()
    post_time = round(post_end_time - post_start_time, 7)

    time_list = [time_for_weather, time_for_elevation, post_time]
    # post.text = Output from POST to server.

    return time_list


def get_end_data():
    return requests.get(URL).json()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def my_form_post():
    city_input = request.form['city']

    time_for_services = post_end_data(city_input)

    get_start_time = time.time()
    get_data = get_end_data()
    get_end_time = time.time()

    get_time = round(get_end_time - get_start_time, 7)
    time_for_services.append(get_time)
    get_plus_post = round(time_for_services[2] + time_for_services[3], 7)
    time_for_services.append(get_plus_post)

    sunrise = get_data['editedSunrise']
    sunset = get_data['editedSunset']
    min_fahrenheit = get_data['fahrenheitTempMin']
    avg_fahrenheit = get_data['fahrenheitTemp']
    max_fahrenheit = get_data['fahrenheitTempMax']
    humidity = get_data['humidity']
    elevation_feet = get_data['elevationFeet']
    visibility_feet = get_data['visibilityFeet']
    country_code = get_data['countryCode']
    weather_description = get_data['weatherDescription']
    windspeed_kmh = get_data['windSpeedKmh']

    return render_template('data.html', avg_fahrenheit=avg_fahrenheit, min_fahrenheit=min_fahrenheit,
                           max_fahrenheit=max_fahrenheit, city=city_input.title(), sunset=sunset,
                           sunrise=sunrise, elevation=elevation_feet, weather_description=weather_description.title(),
                           country_code=country_code, windspeed_kmh=windspeed_kmh, humidity=humidity,
                           visibility_feet=visibility_feet, time_for_services=time_for_services)


if __name__ == '__main__':
    app.run(debug=True, port=8500)
