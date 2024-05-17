import time
import paho.mqtt.client as mqtt_client
from temperatur.ledCtrl import MultiLedCtrl
# import temperatur.ledCtrl


class LedPhase:
    LIGHTBLUE=0
    GREEN=20
    YELLOW=30
    RED=40

class Temp_MQTT:
    def __init__(self):
        self.ledPhase = LedPhase()
        self.multiLedCtrl = MultiLedCtrl(6, 13, 12)
        self.broker_host = "localhost"
        self.broker_port = 1883
        self.client_id = "00ff00"
        
        self.client = self.connect_mqtt()
        self.client.on_message = self.on_message
        # Variant 1: Only publishing:
        self.client.loop_start()

    # Connects to an MQTT broker
    def connect_mqtt(self):
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
        client.username_pw_set(username=self.client_id,password=self.client_id)
        client.on_connect = on_connect
        client.on_disconnect = on_disconnect
        client.connect(self.broker_host, self.broker_port)
        return client

    # Publishes a message to a specific topic with the given client
    def publish(self,msg, topic, client):
        result = client.publish(topic, msg)
        if result[0] == 0:
            print("Published")
        else:
            print("Failed to publish")
            
    # Subscribes to a specific topic with the given client
    def subscribe(self, topic, client):
        client.subscribe(topic)
    # Called when the client receives a message from the broker
    def on_message(self, client, userdata, msg):
        print(f"Received {msg.payload.decode()} from {msg.topic}")
        # Connect and set up on_message callback
   

    def getTemperatur(self):
        tempfile = open("/sys/bus/w1/devices/28-012062311333/w1_slave")
        inhalt = tempfile.read()
        tempfile.close()
        tempdata = inhalt.split("\n")[1].split(" ")[9]
        temperatur = float(tempdata[2:])
        temperatur = temperatur/1000
        print ("Temperatur betraegt: " + str(temperatur) + " Grad")
        
        return temperatur

    def startTemperatur(self):
        try:
            while 1:
                time.sleep(0.5)
                temperatur = self.getTemperatur()
                self.publish(temperatur, "sensor/temperature", self.client)
                
                if(temperatur < self.ledPhase.GREEN):
                    self.multiLedCtrl.lightBlue()
                elif (temperatur >= self.ledPhase.GREEN and temperatur < self.ledPhase.YELLOW):
                    self.multiLedCtrl.green()
                elif (temperatur >= self.ledPhase.YELLOW and temperatur < self.ledPhase.RED):
                    self.multiLedCtrl.yellow()
                elif(temperatur >= self.ledPhase.RED):
                    self.multiLedCtrl.red()
        except KeyboardInterrupt:
            print("") # <--- To make it look better in the console 
            print("End temperature sensor")