from VirtualCopernicusNG import TkCircuit
from pyowm.owm import OWM
from gpiozero import Button, AngularServo
from itertools import cycle
from time import sleep


# initialize the circuit inside the

configuration = {
    "name": "CopernicusNG Weather Forecast",
    "sheet": "sheet_forecast.png",
    "width": 343,
    "height": 267,

    "servos": [
        {"x": 170, "y": 150, "length": 90, "name": "Servo 1", "pin": 17}
    ],
    "buttons": [
        {"x": 295, "y": 200, "name": "Button 1", "pin": 11},
        {"x": 295, "y": 170, "name": "Button 2", "pin": 12},
    ]
}

circuit = TkCircuit(configuration)


# weather data

WEATHER_STATUS = {
    'Clear': -80,
    'Clouds': 10,
    'Drizzle': 35,
    'Rain': 50,
    'Snow': 50,
    'Thunderstorm': 60,
    'Mist': 10,
    'Smoke': 0,
    'Haze': 0,
    'Dust': 0,
    'Fog': 10,
    'Sand': 0,
    'Ash': 0,
    'Squall': 0,
    'Tornado': 70
}

CITIES = cycle({'Istanbul', 'Stockholm'})


@circuit.run
def main():
    # now just write the code you would use on a real Raspberry Pi

    servo1 = AngularServo(17, min_angle=-90, max_angle=90)
    button = Button(12)

    owm = OWM('4526d487f12ef78b82b7a7d113faea64')
    mgr = owm.weather_manager()
    observation = mgr.weather_at_place('Krakow')  # the observation object is a box containing a weather object
    weather = observation.weather

    print(f'Current weather in Krakow: {weather.status}')  # short version of status (eg. 'Rain')

    while True:

        if button.is_pressed:
            city = next(CITIES)
            observation = mgr.weather_at_place(city)
            weather = observation.weather
            print(f'Current weather in {city}: {weather.status}')

        servo1.angle = WEATHER_STATUS[weather.status]
        sleep(0.1)
