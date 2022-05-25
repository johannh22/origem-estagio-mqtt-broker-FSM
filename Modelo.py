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
import paho.mqtt.client as paho
from paho import mqtt
from env_codes import *


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
    def __init__(self, fab):
        super().__init__()
        self.fab = fab
        # random string with 17 chars
        self.chassi = ''.join(random.choice(
            string.ascii_letters) for _ in range(17))
        self.data = {}
        self.topic = f"bike/telemetry/{self.chassi}"
        self.subscribe("bike/telemetry/#")
        self.bat = None

    def communicate(self):
        self.loop_start()
        self.publish(self.topic, payload=json.dumps(
            self.data), qos=1, retain=True)
        self.loop_stop()

    def ask_for_bat(self, supplier):
        self.bat = supplier.supply_bat()
        self.set_data()

    def set_data(self):
        if self.bat:
            self.data = {"id": self.bat.id, "soc": self.bat.soc}

    def get_data(self):
        return self.data


class Bateria:
    def __init__(self):
        self.id = random.randint(1000, 9999)
        self.soc = "fully charged"


class Fabrica:
    def __init__(self):
        self.motos = 0

    def make_moto(self):
        self.motos += 1
        return Moto(self)


class Fornecedor:
    def __init__(self):
        self.bats = 0

    def supply_bat(self):
        self.bats += 1
        return Bateria()
