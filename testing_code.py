import threading, time
import flowclass
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT, initial=GPIO.LOW)	#valve 1
GPIO.setup(23, GPIO.OUT, initial=GPIO.LOW)	#valve 2
GPIO.setup(24, GPIO.OUT, initial=GPIO.LOW)	#valve 3

f1 = flowclass.FlowCalculation(1)
f2 = flowclass.FlowCalculation(2)
f3 = flowclass.FlowCalculation(3)
threading.Timer(1, f1.startSimulation).start()
threading.Timer(1, f2.startSimulation).start()
threading.Timer(1, f3.startSimulation).start()

var = 1
while var!= 0:

    var = input("Enter something: ")
    print("You entered: " + str(var))



