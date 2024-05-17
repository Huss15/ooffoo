import RPi.GPIO as GPIO
class MultiLedCtrl:
        def __init__(self, redLED, greenLED, blueLED):
            self.redLED = redLED
            self.greenLED = greenLED
            self.blueLED = blueLED
            # GPIO Setup
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.redLED, GPIO.OUT)
            GPIO.setup(self.greenLED, GPIO.OUT)
            GPIO.setup(self.blueLED, GPIO.OUT)
            
        def red(self):
            try:
                GPIO.output(self.redLED,GPIO.LOW)
                GPIO.output(self.greenLED,GPIO.HIGH)
                GPIO.output(self.blueLED,GPIO.HIGH)
            except KeyboardInterrupt:
                GPIO.cleanup() 

        def green(self):
            try:
                GPIO.output(self.redLED,GPIO.HIGH)
                GPIO.output(self.greenLED,GPIO.LOW)
                GPIO.output(self.blueLED,GPIO.HIGH)
            except KeyboardInterrupt:
                GPIO.cleanup() 

        
        def lightBlue(self):
            try:
                GPIO.output(self.redLED,GPIO.HIGH)
                GPIO.output(self.greenLED,GPIO.LOW)
                GPIO.output(self.blueLED,GPIO.LOW)
            except KeyboardInterrupt:
                GPIO.cleanup() 
        
        def yellow(self):
            try:
                GPIO.output(self.redLED,GPIO.LOW)
                GPIO.output(self.greenLED,GPIO.LOW)
                GPIO.output(self.blueLED,GPIO.HIGH)
            except KeyboardInterrupt:
                GPIO.cleanup() 