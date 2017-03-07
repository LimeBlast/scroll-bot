# Example of using the MQTT client class to subscribe to and publish feed values.
# Author: Tony DiCola

# Import standard python modules.
import random
import sys
import time
import threading
import os
# import signal

# Import Adafruit IO MQTT client.
from Adafruit_IO import MQTTClient

# Import scrollphathd
import scrollphathd
from scrollphathd.fonts import font5x7

import settings
ADAFRUIT_IO_KEY = os.environ.get("ADAFRUIT_IO_KEY")
ADAFRUIT_IO_USERNAME = os.environ.get("ADAFRUIT_IO_USERNAME")


scrollphathd.rotate(180)

messages = []


def add_message(string):
    messages.append(string)


def display_feed():
    while True:
        if len(messages) > 0:
            print('There are {0} messages waiting for display'.format(len(messages)))
            display_string(messages.pop(0))
        else:
            time.sleep(1)


def display_string(string):
    string += '      '
    buffer = scrollphathd.write_string(string, x=17, y=0, font=font5x7, brightness=0.5)

    for i in range(buffer):
        scrollphathd.show()
        scrollphathd.scroll(1)
        time.sleep(0.02)

    scrollphathd.scroll_to(0, 0)
    scrollphathd.clear()
    scrollphathd.show()


# Define callback functions which will be called when certain events happen.
def connected(client):
    # Connected function will be called when the client is connected to Adafruit IO.
    # This is a good place to subscribe to feed changes.  The client parameter
    # passed to this function is the Adafruit IO MQTT client so you can make
    # calls against it easily.
    print('Connected to Adafruit IO!  Listening for Message changes...')
    # Subscribe to changes on a feed named Message.
    client.subscribe('Message')


def disconnected(client):
    # Disconnected function will be called when the client disconnects.
    print('Disconnected from Adafruit IO!')
    sys.exit(1)


def message(client, feed_id, payload):
    # Message function will be called when a subscribed feed has a new value.
    # The feed_id parameter identifies the feed, and the payload parameter has
    # the new value.
    print('Feed {0} received new value: {1}'.format(feed_id, payload))
    add_message(payload)


# Create an MQTT client instance.
client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Setup the callback functions defined above.
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message

# Connect to the Adafruit IO server.
client.connect()

# Now the program needs to use a client loop function to ensure messages are
# sent and received.  There are a few options for driving the message loop,
# depending on what your program needs to do.

# The first option is to run a thread in the background so you can continue
# doing things in your program.
client.loop_background()

threading.Thread(target=display_feed).start()
