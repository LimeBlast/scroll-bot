import os

import paho.mqtt.client as mqtt

import settings

MQTT_USERNAME = os.environ.get("MQTT_USERNAME")
MQTT_PASSWORD = os.environ.get("MQTT_PASSWORD")
MQTT_HOST = os.environ.get("MQTT_HOST")
MQTT_PORT = os.environ.get("MQTT_PORT")
MQTT_ROOT_TOPIC = os.environ.get("MQTT_ROOT_TOPIC")


# Define event callbacks

def on_connect(client, userdata, rc):
    if rc == 0:
        print("Connected successfully.")
    else:
        print("Connection failed. rc= " + str(rc))


def on_publish(client, userdata, mid):
    print("Message " + str(mid) + " published.")


def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribe with mid " + str(mid) + " received.")


def on_message(client, userdata, msg):
    print("Message received on topic " + msg.topic + " with QoS " + str(msg.qos) + " and payload " + msg.payload.decode(
        "utf-8"))


mqttclient = mqtt.Client()

# Assign event callbacks
mqttclient.on_connect = on_connect
mqttclient.on_publish = on_publish
mqttclient.on_subscribe = on_subscribe
mqttclient.on_message = on_message

# Connect
mqttclient.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
mqttclient.connect(MQTT_HOST, int(MQTT_PORT))

# Start subscription
mqttclient.subscribe(MQTT_ROOT_TOPIC + 'rgb/red')
mqttclient.subscribe(MQTT_ROOT_TOPIC + 'rgb/green')
mqttclient.subscribe(MQTT_ROOT_TOPIC + 'rgb/blue')

mqttclient.loop_forever(timeout=1.0, max_packets=1, retry_first_connection=False)
