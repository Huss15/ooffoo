import time
import paho.mqtt.client as mqtt_client
import RPi.GPIO as GPIO
broker_host = "localhost"
broker_port = 1883
client_id = "00ff00"
redPin = 6
greenPin = 13
bluePin = 12
GPIO.setmode(GPIO.BCM)
lightBluePhase = 0
greenPhase=20
yelowPhase=30
redPhase=40

# GPIO-Pin als Ausgang setzen
GPIO.setmode(GPIO.BCM)
GPIO.setup(redPin, GPIO.OUT)
GPIO.setup(greenPin, GPIO.OUT)
GPIO.setup(bluePin, GPIO.OUT)

def turnOff():
    GPIO.output(redPin,GPIO.HIGH)
    GPIO.output(greenPin,GPIO.HIGH)
    GPIO.output(bluePin,GPIO.HIGH)
    
def white():
    GPIO.output(redPin,GPIO.LOW)
    GPIO.output(greenPin,GPIO.LOW)
    GPIO.output(bluePin,GPIO.LOW)

def red():
    GPIO.output(redPin,GPIO.LOW)
    GPIO.output(greenPin,GPIO.HIGH)
    GPIO.output(bluePin,GPIO.HIGH)

def green():
    GPIO.output(redPin,GPIO.HIGH)
    GPIO.output(greenPin,GPIO.LOW)
    GPIO.output(bluePin,GPIO.HIGH)

    
def lightBlue():
    GPIO.output(redPin,GPIO.HIGH)
    GPIO.output(greenPin,GPIO.LOW)
    GPIO.output(bluePin,GPIO.LOW)
    
def yellow():
    GPIO.output(redPin,GPIO.LOW)
    GPIO.output(greenPin,GPIO.LOW)
    GPIO.output(bluePin,GPIO.HIGH)

# Connects to an MQTT broker
def connect_mqtt():
    # Called after connection attempt
    def on_connect(client, userdata, flags, reason_code, properties):
        if reason_code == 0:
            print("Connected")
        else:
            print("Error connecting. Code:", reason_code)
            # Called after a disconnect
    def on_disconnect(client, userdata, flags, reason_code, properties):
        print("Disconnected:", reason_code)
        # Try to reconnect indefinitely
        while (True):
            time.sleep(5)
            print("Trying to reconnect...")
            try:
                client.reconnect()
                print("Reconnected")
                return
            except Exception as err:
                print("Failed to reconnect:", err)
                # Connect to the broker and set up callbacks
    client = mqtt_client.Client(client_id='',callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2)
    client.username_pw_set(username=client_id,password=client_id)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.connect(broker_host, broker_port)
    return client

# Publishes a message to a specific topic with the given client
def publish(msg, topic, client):
    result = client.publish(topic, msg)
    if result[0] == 0:
        print("Published")
    else:
        print("Failed to publish")
        
# Subscribes to a specific topic with the given client
def subscribe(topic, client):
    client.subscribe(topic)
# Called when the client receives a message from the broker
def on_message(client, userdata, msg):
    print(f"Received {msg.payload.decode()} from {msg.topic}")
    # Connect and set up on_message callback
client = connect_mqtt()
client.on_message = on_message
# Variant 1: Only publishing:
client.loop_start()

try:
    while 1:
        time.sleep(0.5)
        tempfile = open("/sys/bus/w1/devices/28-012062311333/w1_slave")
        inhalt = tempfile.read()
        tempfile.close()
        tempdata = inhalt.split("\n")[1].split(" ")[9]
        temperatur = float(tempdata[2:])
        temperatur = temperatur/1000
        print ("Temperatur betraegt: " + str(temperatur) + " Grad")
        publish(temperatur, "sensor/temperature", client)
        if(temperatur < greenPhase):
            lightBlue()
        elif (temperatur >= greenPhase and temperatur < yelowPhase):
            green()
        elif (temperatur >= yelowPhase and temperatur < redPhase):
            yellow()
        elif(temperatur >= redPhase):
            red()
except KeyboardInterrupt:
    GPIO.cleanup() 


# client.loop_stop()
# Variant 2: Only subscribing:
# subscribe("Some topic", client)
# client.loop_forever()