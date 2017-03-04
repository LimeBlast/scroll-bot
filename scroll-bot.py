# Example of using the MQTT client class to subscribe to and publish feed values.
# Author: Tony DiCola

# Import standard python modules.
import random
import sys
import time
# import signal

# Import Adafruit IO MQTT client.
from Adafruit_IO import MQTTClient

# Import scrollphathd
import scrollphathd
from scrollphathd.fonts import font5x7

# Set to your Adafruit IO key & username below.
ADAFRUIT_IO_KEY = '1168c7db061e42b29aa7f9e32af5ad42'
ADAFRUIT_IO_USERNAME = 'LimeBlast'  # See https://accounts.adafruit.com
# to find your username.

scrollphathd.rotate(180)

# Define callback functions which will be called when certain events happen.
def connected(client):
    # Connected function will be called when the client is connected to Adafruit IO.
    # This is a good place to subscribe to feed changes.  The client parameter
    # passed to this function is the Adafruit IO MQTT client so you can make
    # calls against it easily.
    print('Connected to Adafruit IO!  Listening for DemoFeed changes...')
    # Subscribe to changes on a feed named DemoFeed.
    client.subscribe('DemoFeed')


def disconnected(client):
    # Disconnected function will be called when the client disconnects.
    print('Disconnected from Adafruit IO!')
    sys.exit(1)


def message(client, feed_id, payload):
    # Message function will be called when a subscribed feed has a new value.
    # The feed_id parameter identifies the feed, and the payload parameter has
    # the new value.
    print('Feed {0} received new value: {1}'.format(feed_id, payload))

    scrollphathd.clear()
    scrollphathd.write_string(payload, x=0, y=0, font=font5x7, brightness=0.5)

    status_length = len(payload)
    while status_length > 0:
        scrollphathd.show()
        scrollphathd.scroll()
        time.sleep(0.1)
        status_length -= 1


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

# Now send new values every 10 seconds.
print('Publishing a new message every 10 seconds (press Ctrl-C to quit)...')
while True:
    value = random.randint(0, 100)
    print('Publishing {0} to DemoFeed.'.format(value))
    client.publish('DemoFeed', value)
    time.sleep(10)
