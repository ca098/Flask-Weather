import parser
import time
from flask import Flask, request
from flask_restful import Resource, Api, abort
import datetime

app = Flask(__name__)

api = Api(app)

# Initialise two objects to handle requests.
JSON_OBJECT = {}

PROCESSED_OBJECT = {}


def abort_if_task_doesnt_exist(task_id):
    if task_id not in PROCESSED_OBJECT:
        abort(404, message="Id {} doesn't exist".format(task_id))


class Server(Resource):

    def get(self):
        """ Stripping the posted object, and populating a new object with only the relevant data required.
         Data is processed by the server to be sent back in the GET request. """
        min_fahrenheit = round(JSON_OBJECT['postedData']['main']['temp_min'] * 9 / 5 + 32, 2)
        avg_fahrenheit = round(JSON_OBJECT['postedData']['main']['temp'] * 9 / 5 + 32, 2)
        max_fahrenheit = round(JSON_OBJECT['postedData']['main']['temp_max'] * 9 / 5 + 32, 2)
        humidity = "{}/100".format(JSON_OBJECT['postedData']['main']['humidity'])
        time_zone = JSON_OBJECT['postedData']['timezone']  # of GMT

        sunset = time.strftime('%H:%M:%S', time.localtime(JSON_OBJECT['postedData']['sys']['sunset'] + time_zone))
        sunrise = time.strftime('%H:%M:%S', time.localtime(JSON_OBJECT['postedData']['sys']['sunrise'] + time_zone))
        elevation_feet = round(JSON_OBJECT['postedData']['height'] * 3.28084)
        visibility_feet = round(int(JSON_OBJECT['postedData']['visibility']) * 3.28084)
        country_code = JSON_OBJECT['postedData']['sys']['country']
        weather_description = JSON_OBJECT['postedData']['weather'][0]['description']
        wind_speed_kmh = round(JSON_OBJECT['postedData']['wind']['speed'] * 1.60934)
        city = JSON_OBJECT['postedData']['name']

        ts = time.time()

        # Populating the blank object with processed data from the POST request.
        PROCESSED_OBJECT['editedSunrise'] = sunrise
        PROCESSED_OBJECT['editedSunset'] = sunset
        PROCESSED_OBJECT['fahrenheitTempMin'] = min_fahrenheit
        PROCESSED_OBJECT['fahrenheitTemp'] = avg_fahrenheit
        PROCESSED_OBJECT['fahrenheitTempMax'] = max_fahrenheit
        PROCESSED_OBJECT['humidity'] = humidity
        PROCESSED_OBJECT['elevationFeet'] = elevation_feet
        PROCESSED_OBJECT['visibilityFeet'] = visibility_feet
        PROCESSED_OBJECT['countryCode'] = country_code
        PROCESSED_OBJECT['weatherDescription'] = weather_description
        PROCESSED_OBJECT['windSpeedKmh'] = wind_speed_kmh
        PROCESSED_OBJECT['city'] = city
        PROCESSED_OBJECT['timeZone'] = time_zone / 3600
        PROCESSED_OBJECT['timeStamp'] = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y %H:%M:%S')

        return PROCESSED_OBJECT

    def post(self):
        # Populate the empty object that has already been initialised above, with the POST data from the client.
        JSON_OBJECT['postedData'] = request.get_json()
        return {'you sent': JSON_OBJECT}, 201


class Edit(Resource):

    # Data must be posted from client before initialising PUT & DELETE methods.
    def put(self, task_id):
        args = parser.parse_args()
        task = {'task': args['task']}
        PROCESSED_OBJECT[task_id] = task
        return task, 201

    def delete(self, task_id):
        self.abort_if_task_doesnt_exist(task_id)
        del PROCESSED_OBJECT[task_id]
        return '', 204


api.add_resource(Server, '/details/')
api.add_resource(Edit, '/edit/<string:task_id>')

if __name__ == '__main__':
    app.run(debug=True)
