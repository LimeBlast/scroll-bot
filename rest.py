from Adafruit_IO import *

key = '1168c7db061e42b29aa7f9e32af5ad42'
aio = Client(key)
# mqtt = MQTTClient(key)

# Send the value 100 to a feed called 'Foo'.
aio.send('Foo', 77)

# Retrieve the most recent value from the feed 'Foo'.
# Access the value by reading the `value` property on the returned Data object.
# Note that all values retrieved from IO are strings so you might need to convert
# them to an int or numeric type if you expect a number.
data = aio.receive('Foo')
print('Received value: {0}'.format(data.value))
