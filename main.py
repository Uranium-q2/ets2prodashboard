import os
from flask import Flask, render_template, jsonify
import urllib.request
import json

app = Flask(__name__)

ETS2_API_URL = os.environ.get('ETS2_API_URL', 'http://host.docker.internal:25555/api/ets2/telemetry')

EMPTY_RESPONSE = {
    'connected': False,
    'speed': 0,
    'rpm': 0,
    'fuel': 0,
    'fuel_capacity': 1,
    'fuel_percent': 0,
    'fuel_range_km': 0,
    'temp': 0,
    'gear': '---',
    'cruise_speed': 0,
    'cruise_on': False,
    'blinker_left': False,
    'blinker_right': False,
    'parking_brake': False,
    'engine_on': False,
    'electric_on': False,
    'lights_parking': False,
    'lights_low_beam': False,
    'lights_high_beam': False,
    'lights_hazard': False,
    'wipers': False,
    'odometer': 0,
    'trailer_attached': False,
    'damage_engine': 0,
    'damage_transmission': 0,
    'damage_cabin': 0,
    'damage_chassis': 0,
    'damage_wheels': 0,
    'job_active': False,
    'job_cargo': '',
    'job_source': '',
    'job_destination': '',
    'job_income': 0,
    'job_distance_km': 0,
    'game_time': '',
}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/data')
def get_data():
    try:
        req = urllib.request.Request(ETS2_API_URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=0.5) as response:
            data = json.loads(response.read().decode('utf-8'))

            truck = data.get('truck', {})
            trailer = data.get('trailer', {})
            controls = data.get('controls', {})
            job = data.get('job', {})
            navigation = data.get('navigation', {})
            game = data.get('game', {})

            speed_kmh = max(0, int(truck.get('speed', 0.0)))
            rpm = int(truck.get('engineRpm', 0))
            fuel = truck.get('fuel', 0)
            fuel_capacity = truck.get('fuelCapacity', 0) or 1
            fuel_avg_consumption = truck.get('fuelAverageConsumption', 0) or 0
            fuel_percent = round((fuel / fuel_capacity) * 100, 1) if fuel_capacity else 0
            fuel_range_km = int(fuel / fuel_avg_consumption) if fuel_avg_consumption else 0
            temp = truck.get('engineTemperature', 0)

            raw_gear = truck.get('displayedGear', 0)
            if raw_gear == 0:
                gear_str = 'N'
            elif raw_gear < 0:
                gear_str = f'R{abs(raw_gear)}'
            else:
                gear_str = str(raw_gear)

            cc_on = truck.get('cruiseControlOn', False)
            cc_speed = int(truck.get('cruiseControlSpeed', 0) * 3.6) if cc_on else 0

            blinker_left = controls.get('blinkerLeftActive', False)
            blinker_right = controls.get('blinkerRightActive', False)

            job_remaining_distance = navigation.get('estimatedDistance', 0)
            job_remaining_time_min = navigation.get('estimatedTime', 0)

            return jsonify({
                'connected': True,
                'speed': speed_kmh,
                'rpm': rpm,
                'fuel': round(fuel, 1),
                'fuel_capacity': round(fuel_capacity, 1),
                'fuel_percent': fuel_percent,
                'fuel_range_km': fuel_range_km,
                'temp': temp,
                'gear': gear_str,
                'cruise_speed': cc_speed,
                'cruise_on': cc_on,
                'blinker_left': blinker_left,
                'blinker_right': blinker_right,
                'parking_brake': truck.get('parkingBrakeOn', False),
                'engine_on': truck.get('engineEnabled', False),
                'electric_on': truck.get('electricEnabled', False),
                'lights_parking': truck.get('lightsParkingOn', False),
                'lights_low_beam': truck.get('lightsBeamLowOn', False),
                'lights_high_beam': truck.get('lightsBeamHighOn', False),
                'lights_hazard': truck.get('lightsHazardOn', False),
                'wipers': truck.get('wipersOn', False),
                'odometer': int(truck.get('odometer', 0)),
                'trailer_attached': trailer.get('attached', False),
                'damage_engine': round(truck.get('engineDamage', 0) * 100),
                'damage_transmission': round(truck.get('transmissionDamage', 0) * 100),
                'damage_cabin': round(truck.get('cabinDamage', 0) * 100),
                'damage_chassis': round(truck.get('chassisDamage', 0) * 100),
                'damage_wheels': round(truck.get('wheelsDamage', 0) * 100) if isinstance(truck.get('wheelsDamage', 0), (int, float)) else 0,
                'job_active': bool(job.get('income')) or job_remaining_distance > 0,
                'job_cargo': job.get('cargo', ''),
                'job_source': job.get('sourceCity', ''),
                'job_destination': job.get('destinationCity', ''),
                'job_income': job.get('income', 0),
                'job_distance_km': int(job_remaining_distance / 1000) if job_remaining_distance else 0,
                'job_time_min': int(job_remaining_time_min) if job_remaining_time_min else 0,
                'game_time': game.get('time', ''),
            })
    except Exception:
        return jsonify(EMPTY_RESPONSE)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
