import threading, time
import flowclass
import copy
import RPi.GPIO as GPIO
from bs4 import BeautifulSoup

#GPIO.setmode(GPIO.BCM)
#GPIO.setup(18, GPIO.OUT, initial=GPIO.LOW)	#valve 1
#GPIO.setup(23, GPIO.OUT, initial=GPIO.LOW)	#valve 2
#GPIO.setup(24, GPIO.OUT, initial=GPIO.LOW)	#valve 3

def modify_drink_num(f,drink_number):
    df = copy.deepcopy(f.keg_stats)
    print('pour_check: ' + str(df['pour_check']))
    return
    

f1 = flowclass.FlowCalculation(1)
f2 = flowclass.FlowCalculation(2)
f3 = flowclass.FlowCalculation(3)
f1.scheduleSimulation()
f2.scheduleSimulation()
f3.scheduleSimulation()
# fs = [f1,f2,f3]
# for f in fs:
    # ff = f
    # print(f.valve_num)

modify_drink_num(f1,20)
# ff.drink_num = 20
# print(f1.drink_num)
# print(f2.drink_num)
# print(f3.drink_num)
# print(ff.drink_num))
var = 1
while var!= 0:
    var = input("Enter something: ")
    print(threading.active_count())
    if(var == 1):
        f1.cancel_valve()
    if(var == 2):
        f2.cancel_valve()
    if(var == 3):
        f3.cancel_valve()
    


