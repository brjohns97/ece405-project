#comment
import RPi.GPIO as GPIO
import time, sys
import math
GPIO.setmode(GPIO.BCM)
inpt = 27
GPIO.setup(inpt, GPIO.IN)
GPIO.setup(18, GPIO.OUT)

pour_time = 0.0
time_start = 0.0
time_end = 0.0
gpio_last = 0
pulses = 0
constant = 6.5
total_time = 0.0
volume = 0

print('Water Flow - Approximate')
#print(math.ceil(math.pi/2))

#GPIO.output(18, GPIO.HIGH)
while True:
    pulses = 0
    pour_time = 0
    time_start = time.time()
    while pulses <=5:
        gpio_cur = GPIO.input(inpt)
        if gpio_cur != 0 and gpio_cur != gpio_last:
            pulses += 1
        gpio_last = gpio_cur
        print(GPIO.input(27), end='')


    time_end = time.time()
    pour_time = time_end-time_start
    frequency = pulses/(pour_time)
    Q = frequency/constant
    volume = volume + Q*(pour_time/60)
    total_time = total_time + pour_time
    print('Frequency: ',round(frequency,2))
    print('Liters / min',round(Q,2),'approximate')
    print('Total Liters ', round(volume,2))
    print('Time (seconds & clock)',round(total_time,2), '\t',time.asctime(time.localtime(time.time())),'\n')
            
#GPIO.output(18, GPIO.LOW)

            
            
            
            
            
            
            
            
            
