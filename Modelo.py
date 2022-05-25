#
# ! NOTICE: this file (the MQTT part) was adapted from mqtt_client.py
# ! be found in the HiveMQ website.
#
# MODELO
# This file contains the requested model, with the following classes:
#     * Moto
#     * Bateria
#     * Fabrica
#     * Fornecedor
#
# The documentation used for paho is located at https://www.hivemq.com/blog/mqtt-client-library-paho-python/ and on HiveMQ's getting started guide
#
# See https://www.apache.org/licenses/LICENSE-2.0 for license details
#

import json
import string
import random
import time
import paho.mqtt.client as paho
from paho import mqtt
from env_codes import *

STATES = [("off"), "on", "drawer_open", "running"]

class MotoClient(paho.Client):
    def __init__(self, client_id=CLIENT_ID,
                 userdata=None, protocol=paho.MQTTv5):
        super().__init__(client_id,
                         userdata, protocol)
        # enable TLS for secure connection
        self.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
        self.username_pw_set(USER, PASSWORD)
        self.connect(HOST_NAME, 8883)

    def on_connect(self, client, userdata, flags, rc, properties=None):
        print(f"CONNACK received with code {str(rc)}.")

    def on_publish(self, client, userdata, message_id, properties=None):
        print("message id: " + str(message_id))

    def on_subscribe(self, client, userdata, message_id, granted_qos, properties=None):
        print("Subscribed: " + str(message_id) + " " + str(granted_qos))

    def on_message(self, client, userdata, msg):
        print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


# Moto inherits from MotoClient in order to use MQTT
class Moto(MotoClient):
    def __init__(self, fab, supplier):
        super().__init__()
        self.fab = fab
        # random string with 17 chars
        self.chassi = ''.join(random.choice(
            string.ascii_letters) for _ in range(17))
        self.data = {}
        self.topic = f"bike/telemetry/{self.chassi}"
        self.subscribe("bike/telemetry/#")
        self.bat = None
        self.state = "off"
        self.km = 0
        self.supplier = supplier

    def get_state(self):
        return self.state

    def communicate(self):
        """Update data then publish telemetry"""
        self.set_data()
        self.loop_start()
        self.publish(self.topic, payload=json.dumps(
            self.data), qos=1, retain=True)
        self.loop_stop()

    def ask_for_bat(self):
        if self.state != "drawer_open":
            print("Please open drawer first")
        else:
            self.bat = self.supplier.supply_bat()
            self.set_data()
            print("Battery successfuly inserted")

    def remove_bat(self):
        if self.state != "drawer_open":
            print("Please open drawer first")
        else:
            self.bat = None
            self.data = {}

    def set_data(self):
        if self.bat:
            self.data = {"id": self.bat.id, "soc": self.bat.soc}

    def get_data(self):
        return self.data

    def off(self):
        print("Turning motorcycle off")
        self.state = "off"

    def on(self):
        if self.state == "off":
            print("Turning motorcycle on")
            self.state = "on"
        else:
            print("Motorcycle already on")

    def open_drawer(self):
        if self.state == "on":
            print("Opening drawer")
            self.state = "drawer_open"
        elif self.state == "off":
            print("Please, turn motorcycle on first")
        elif self.state == "drawer_open":
            print("Drawer already open")

    def close_drawer(self):
        if self.state == "drawer_open":
            print("Closing drawer")
            self.state = "on"
        else:
            print("Drawer already closed")

    def ignite(self):
        if self.state == "off":
            print("Motorcycle must be turned on first")
        elif not self.bat:
            print("Please insert battery first")
        elif self.state == "on":
            print("Engines on, power up!")
            self.state = "running"
            self.run()
        elif self.state == "drawer_open":
            print("Drawer must be closed first")

    def run(self):
        """Function that runs the motorcycle. I tried some solutions to make
        the keyboard control this process, but couldn't get around the problem
        related tracking and time and simultaneously monitoring the keyboard. I
        tried using pynput and learning multithreading for this, but didn't get
        to a nice solution. If you guys know any, please tell me =)
        The most succint way I found was to just ask every 15 seconds if the
        user wants to change the state, although I don't like the idea of pausing the program so often..."""
        print("Motorcycle running")
        stop = False
        count = 0
        while not stop:
            time.sleep(5)  # wait 5 seconds
            count += 1
            self.bat.soc -= 1
            self.km += 1
            self.communicate()
            if self.bat.soc == 10:
                print("Battery percentage running low, now 10%. Please charge.")
            elif self.bat.soc == 0:
                print("Battery out of charge.")
                self.off()
                stop = True
            elif count == 3:
                count = 0
                action = input(
                    "Do you want to change state?\n- 'o' + 'enter' for 'off'\n- 'p' + 'enter' for 'on'\n- any other key + 'enter' to continue\n")
                if action == 'o':
                    self.off()
                    stop = True
                elif action == 'p':
                    self.on()
                    stop = True
                else:
                    print("Heading out to the highway!")


class Bateria:
    def __init__(self):
        self.id = random.randint(1000, 9999)
        self.soc = 100


class Fabrica:
    def __init__(self):
        self.motos = 0

    def make_moto(self, supplier):
        # Tie the supplier to the motorcycle
        self.motos += 1
        return Moto(self, supplier)


class Fornecedor:
    def __init__(self):
        self.bats = 0

    def supply_bat(self):
        self.bats += 1
        return Bateria()
