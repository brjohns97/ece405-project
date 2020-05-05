import RPi.GPIO as GPIO
import time
import threading
import sys

start_check = 0

def myFunc():
    count = threading.active_count()
    print("Thread Count: ", count)
    print(threading.enumerate())
    threading.Timer(5,myFunc).start()
    
count = threading.active_count()
print("Thread Count: ", count)
print(threading.enumerate())
while True:
    try:
        if(start_check == 0):
            count = threading.active_count()
            print("Thread Count: ", count)
            print(threading.enumerate())
            start_check=1
            threading.Timer(1,myFunc).start()
    except KeyboardInterrupt:
        sys.exit()
# GPIO.setmode(GPIO.BCM)
# GPIO.setwarnings(False)
# GPIO.setup(4,GPIO.OUT)
# print("LED on")
# GPIO.output(4,GPIO.HIGH)
# time.sleep(5)
# print("LED off")
# GPIO.output(4,GPIO.LOW)