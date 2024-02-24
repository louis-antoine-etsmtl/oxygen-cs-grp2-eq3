from signalrcore.hub_connection_builder import HubConnectionBuilder
import logging
import requests
import json
import time
import os

from dotenv import load_dotenv

class Main:
    def __init__(self):

        # Load environment variables from .env file
        load_dotenv()

        self.DATABASE = os.getenv('DATABASE_URL')
        # Check if the environment variable is set
        if self.DATABASE is not None:
            print(f'Database URL: {self.DATABASE}')
        else:
            print('DATABASE_URL is not set. Please set the environment variable.')

        self.HOST = os.getenv('HOST')
        # Check if the environment variable is set
        if self.HOST is not None:
            print(f'HOST URL: {self.HOST}')
        else:
            print('HOST is not set. Please set the environment variable.')

        self._hub_connection = os.getenv('HUB_CONNECTION')
        # Check if the environment variable is set
        if self._hub_connection is not None:
            print(f'_hub_connection: {self._hub_connection}')
        else:
            print('_hub_connection is not set. Please set the environment variable.')

        self.TOKEN = os.getenv('TOKEN')
        # Check if the environment variable is set
        if self.TOKEN is not None:
            print(f'TOKEN: {self.TOKEN}')
        else:
            print('TOKEN is not set. Please set the environment variable.')

        self.TICKETS = os.getenv('TICKETS')
        # Check if the environment variable is set
        if self.TICKETS is not None:
            print(f'TICKETS: {self.TICKETS}')
        else:
            print('TICKETS is not set. Please set the environment variable.')

        self.T_MAX = os.getenv('T_MAX')
        # Check if the environment variable is set
        if self.T_MAX is not None:
            print(f'T_MAX: {self.T_MAX}')
        else:
            print('T_MAX is not set. Please set the environment variable.')

        self.T_MIN = os.getenv('T_MIN')
        # Check if the environment variable is set
        if self.T_MIN is not None:
            print(f'T_MIN: {self.T_MIN}')
        else:
            print('T_MIN is not set. Please set the environment variable.')



    def __del__(self):
        if self._hub_connection != None:
            self._hub_connection.stop()

    def setup(self):
        """Setup Oxygen CS."""
        self.set_sensorhub()

    def start(self):
        """Start Oxygen CS."""
        self.setup()
        self._hub_connection.start()

        print("Press CTRL+C to exit.", flush=True)
        while True:
            time.sleep(2)

    def set_sensorhub(self):
        """Configure hub connection and subscribe to sensor data events."""
        self._hub_connection = (
            HubConnectionBuilder()
            .with_url(f"{self.HOST}/SensorHub?token={self.TOKEN}")
            .configure_logging(logging.INFO)
            .with_automatic_reconnect(
                {
                    "type": "raw",
                    "keep_alive_interval": 10,
                    "reconnect_interval": 5,
                    "max_attempts": 999,
                }
            )
            .build()
        )

        self._hub_connection.on("ReceiveSensorData", self.on_sensor_data_received)
        self._hub_connection.on_open(lambda: print("||| Connection opened.", flush=True))
        self._hub_connection.on_close(lambda: print("||| Connection closed.", flush=True))
        self._hub_connection.on_error(
            lambda data: print(f"||| An exception was thrown closed: {data.error}", flush=True)
        )

    def on_sensor_data_received(self, data):
        """Callback method to handle sensor data on reception."""
        try:
            print(data[0]["date"] + " --> " + data[0]["data"], flush=True)
            date = data[0]["date"]
            temperature = float(data[0]["data"])
            self.take_action(temperature)
        except Exception as err:
            print(err, flush=True)

    def take_action(self, temperature):
        """Take action to HVAC depending on current temperature."""
        if float(temperature) >= float(self.T_MAX):
            self.send_action_to_hvac("TurnOnAc")
        elif float(temperature) <= float(self.T_MIN):
            self.send_action_to_hvac("TurnOnHeater")

    def send_action_to_hvac(self, action):
        """Send action query to the HVAC service."""
        r = requests.get(f"{self.HOST}/api/hvac/{self.TOKEN}/{action}/{self.TICKETS}")
        details = json.loads(r.text)
        print(details, flush=True)

    def send_event_to_database(self, timestamp, event):
        """Save sensor data into database."""
        try:
            # To implement
            pass
        except requests.exceptions.RequestException as e:
            # To implement
            pass


if __name__ == "__main__":
    main = Main()
    main.start()
