import threading, time
import flowclass
import copy
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT, initial=GPIO.LOW)	#valve 1
GPIO.setup(23, GPIO.OUT, initial=GPIO.LOW)	#valve 2
GPIO.setup(24, GPIO.OUT, initial=GPIO.LOW)	#valve 3

def modify_drink_num(f,drink_number):
    df = copy.deepcopy(f)
    df.drink_num = drink_number;
    return df
    

f1 = flowclass.FlowCalculation(1)
f2 = flowclass.FlowCalculation(2)
f3 = flowclass.FlowCalculation(3)
#threading.Timer(1, f1.startSimulation).start()
#threading.Timer(1, f2.startSimulation).start()
#threading.Timer(1, f3.startSimulation).start()

fs = [f1,f2,f3]

for f in fs:
    ff = f
    print(f.valve_num)

ff.drink_num = 20
print(f1.drink_num)
print(f2.drink_num)
print(f3.drink_num)
print(ff.drink_num)
#var = 1
# while var!= 0:

    # var = input("Enter something: ")
    # print("You entered: " + str(var))



