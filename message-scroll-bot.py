# Import standard python modules.
import sys
import time
import threading
import os
import queue

# Import Adafruit IO MQTT client.
from Adafruit_IO import MQTTClient

# Import scrollphathd
import scrollphathd
from scrollphathd.fonts import font5x7

import settings

ADAFRUIT_IO_KEY = os.environ.get("ADAFRUIT_IO_KEY")
ADAFRUIT_IO_USERNAME = os.environ.get("ADAFRUIT_IO_USERNAME")

scrollphathd.rotate(180)

messages = queue.Queue()
queue_processor_running = False


def add_message(string):
    messages.put(string)


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


def process_next_queue_item():
    display_string(messages.get())


def start_queue_processor():
    queue_processor_running = True
    print('Starting up queue')
    while True:
        if messages.qsize() == 0:
            queue_processor_running = False
            print('Shutting down queue')
            break
        process_next_queue_item()
        time.sleep(1)


def connected(client):
    print('Connected to Adafruit IO!  Listening for Message changes...')
    client.subscribe('Message')


def disconnected(client):
    print('Disconnected from Adafruit IO!')
    sys.exit(1)


def message(client, feed_id, payload):
    print('Feed {0} received new value: {1}'.format(feed_id, payload))
    add_message(payload)
    if not queue_processor_running:
        start_queue_processor()


# Create an MQTT client instance.
client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Setup the callback functions defined above.
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message

# Connect to the Adafruit IO server.
client.connect()

# This will run a message loop forever, so your program
# will not get past the loop_blocking call.  This is
# good for simple programs which only listen to events.
client.loop_blocking()
