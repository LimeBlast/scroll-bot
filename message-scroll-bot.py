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


def start_queue_processor():
    # This is running in a background thread. So it's safe to block.
    # Basically, it blocks until a message shows up in the queue,
    # and then displays it, and then waits five seconds.
    # So things can accumulate in the queue without a problem, and
    # this will just process them when it gets to them; if there's
    # nothing in the queue, this will block on the next_message
    # line until there is something in the queue.
    while True:
        print("[Queue] waiting for message")
        next_message = messages.get() # this blocks!
        print("[Queue] got a message (there are %s messages still in the queue)" % (messages.qsize(),))
        display_string(next_message)
        time.sleep(5) # and wait around a bit so you can read the message


def connected(client):
    print('Connected to Adafruit IO!  Listening for Message changes...')
    client.subscribe('Message')


def disconnected(client):
    print('Disconnected from Adafruit IO!')
    sys.exit(1)


def message(client, feed_id, payload):
    print('Feed {0} received new value: {1}'.format(feed_id, payload))
    messages.put(payload)

# Start the queue processor in a background thread
queuethread = threading.Thread(target=start_queue_processor)
queuethread.setDaemon(True) # ensure that when the main loop exits, the bgthread exits too
queuethread.start()


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
