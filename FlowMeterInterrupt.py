#comment
import RPi.GPIO as GPIO
import time, sys, math

GPIO.setmode(GPIO.BCM)       #refers to gpio #, not pin #
GPIO.setup(27, GPIO.IN)
GPIO.setup(18, GPIO.OUT)
time.sleep(1)
pour_time = 0.0
time_start = 0.0
time_end = 0.0
max_pulse = 3
pulse = max_pulse
update_flag = 0
constant = 6.5
total_time = 0.0
total_volume = 0
desired_volume = 50*0.0295735
Q = 0
Q1 = 0
Q2 = 0
Q3 = 0
first_rising_edge = 0

def my_callback(channel):
    global time_start,time_end,pulse,update_flag,max_pulse,pour_time

    if (pulse == max_pulse):
        time_end = time.time()
        pour_time = time_end - time_start
        time_start = time.time()
        update_flag = 1
        pulse = 0

    pulse += 1


GPIO.add_event_detect(27, GPIO.RISING, callback=my_callback)

print('Water Flow - Approximate')
GPIO.output(18, GPIO.HIGH)

while (total_volume < desired_volume):
    try:
        if(update_flag == 1 and first_rising_edge != 0):
            update_flag = 0
            frequency = (max_pulse)/(pour_time)
            Q3 = Q2
            Q2 = Q1
            Q1 = Q
            Q = frequency/constant
            total_volume = total_volume + Q*(pour_time/60)
            total_time = total_time + pour_time
            print('Frequency: ',round(frequency,2))
            print('Liters / min',round(Q,2),'approximate')
            print('Total Liters ', round(total_volume,2))
            print('Time (seconds & clock)',round(total_time,2), '\t',time.asctime(time.localtime(time.time())),'\n')
        if(update_flag == 1 and first_rising_edge == 0):
            update_flag = 0
            first_rising_edge = 1
        None
    except KeyboardInterrupt:
        GPIO.cleanup()
        sys.exit()
        
GPIO.output(18, GPIO.LOW)
timeout = time.time() + 5
print("====Entering other while loop====")
while (time.time() < timeout):
    try:
        if(update_flag == 1 and first_rising_edge != 0):
            update_flag = 0
            frequency = (max_pulse)/(pour_time)
            Q3 = Q2
            Q2 = Q1
            Q1 = Q
            Q = frequency/constant
            total_volume = total_volume + Q*(pour_time/60)
            total_time = total_time + pour_time
            print('Frequency: ',round(frequency,2))
            print('Liters / min',round(Q,2),'approximate')
            print('Total Liters ', round(total_volume,2))
            print('Time (seconds & clock)',round(total_time,2), '\t',time.asctime(time.localtime(time.time())),'\n')
        None
    except KeyboardInterrupt:
        GPIO.cleanup()
        sys.exit()

diff_volume = total_volume-desired_volume
diff_seconds = (diff_volume/((Q3+Q2+Q1)/3))*60
time.sleep(2)
print('Difference in volume (liters):',diff_volume)
print('Difference in stop times (seconds):',diff_seconds)







            
