import os
import time
import logging
import requests
import psycopg2
from dotenv import load_dotenv
from signalrcore.hub_connection_builder import HubConnectionBuilder


class App:
    def __init__(self):
        load_dotenv()  # Load environment variables from .env file

        # Mandatory environment variables. These will raise an exception if not set
        self.DATABASE = os.getenv("DATABASE_URL")
        self.HOST = os.getenv("HOST")
        self.TOKEN = os.getenv("TOKEN")
        self.T_MAX = int(os.getenv("T_MAX"))
        self.T_MIN = int(os.getenv("T_MIN"))
        self.TICKETS = int(os.getenv("TICKETS"))
        self._hub_connection = os.getenv("HUB_CONNECTION")

        print("self.DATABASE ==> " + self.DATABASE)
        print("self.HOST ==> " + self.HOST)
        print("self.TOKEN ==> " + self.TOKEN)

        print("self.HUB_CONNECTION ==> " + os.getenv("HUB_CONNECTION"))
        print("self.T_MAX ==> " + str(self.T_MAX))
        print("self.T_MIN ==> " + str(self.T_MIN))
        print("self.TICKETS ==> " + str(self.TICKETS))
        print("self.HUB_CONNECTION ==> " + self._hub_connection)
        # Ensure all mandatory environment variables are set
        mandatory_vars = ["DATABASE", "HOST", "TOKEN", "T_MAX", "T_MIN", "TICKETS"]
        for var in mandatory_vars:
            if getattr(self, var) is None:
                raise ValueError(
                    f"{var} is not set. Please set the environment variable."
                )

        self._hub_connection = None

    def __del__(self):
        if self._hub_connection is not None:
            self._hub_connection.stop()

    def start(self):
        """Start Oxygen CS."""
        self.setup_sensor_hub()
        self._hub_connection.start()
        print("Press CTRL+C to exit.")
        while True:
            time.sleep(2)

    def setup_sensor_hub(self):
        try:
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

            print("_hub_connection =====>" + str(self._hub_connection))
            self._hub_connection.on("ReceiveSensorData", self.on_sensor_data_received)
            self._hub_connection.on_open(lambda: print("||| Connection opened."))
            self._hub_connection.on_close(lambda: print("||| Connection closed."))
            self._hub_connection.on_error(
                lambda data: print(f"||| An exception was thrown closed: {data.error}")
            )
        except Exception as e:
            logger.error(f"Error establishing SignalR connection: {e}")
            logger.error(traceback.format_exc())

    def on_sensor_data_received(self, data):
        """Callback method to handle sensor data on reception."""
        try:
            print(data[0]["date"] + " --> " + data[0]["data"], flush=True)
            timestamp = data[0]["date"]
            temperature = float(data[0]["data"])
            self.take_action(temperature)
            self.save_event_to_database(timestamp, temperature)
        except Exception as err:
            print(err)

    def save_event_to_database(self, timestamp, temperature):
        """Enregistrer les données de capteur dans la base de données."""
        connection = None
        try:
            connection = psycopg2.connect(self.DATABASE)
            cursor = connection.cursor()

            # Insertion des données de température
            insert_sensor_data_query = """
            INSERT INTO SENSOR_DATA (timestamp, temperature) VALUES (%s, %s);
            """
            cursor.execute(insert_sensor_data_query, (timestamp, temperature))
            connection.commit()
            print(f"Sensor data saved to database: {timestamp}, {temperature}")

        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Erreur lors de l'enregistrement dans la base de données: {error}")
        finally:
            if connection:
                cursor.close()
                connection.close()

    def take_action(self, temperature):
        """Take action to HVAC depending on current temperature."""
        if float(temperature) >= float(self.T_MAX):
            print(f"Temperature {temperature} >= {self.T_MAX}: Turning on AC.")
            self.send_action_to_hvac("TurnOnAc")
        elif float(temperature) <= float(self.T_MIN):
            print(f"Temperature {temperature} <= {self.T_MIN}: Turning on Heater.")
            self.send_action_to_hvac("TurnOnHeater")

    def send_action_to_hvac(self, action):
        """Envoyer une action au service HVAC et enregistrer l'événement."""
        try:
            response = requests.get(
                f"{self.HOST}/api/hvac/{self.TOKEN}/{action}/{self.TICKETS}", timeout=5
            )
            if response.status_code == 200:
                details = response.json()
                print(f"Action {action} sent to HVAC, response: {details}")
                # Enregistrez l'événement HVAC après avoir envoyé l'action
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                self.save_hvac_event_to_database(timestamp, action)
            else:
                print(f"Failed to send action {action} to HVAC: {response.status_code}")
        except Exception as e:
            print(f"Exception while sending action {action} to HVAC: {e}")

    def save_hvac_event_to_database(self, timestamp, event_type):
        """Enregistrer les événements HVAC dans la base de données."""
        try:
            with psycopg2.connect(self.DATABASE) as conn:
                with conn.cursor() as cursor:
                    insert_query = """
                    INSERT INTO HVAC_EVENTS (timestamp, event_type) VALUES (%s, %s);
                    """
                    cursor.execute(insert_query, (timestamp, event_type))
                    print(f"HVAC event {event_type} saved to database: {timestamp}")
        except Exception as e:
            print(f"Error saving HVAC event {event_type} to database: {e}")
            print("hello")


if __name__ == "__main__":
    app = App()
    app.start()
