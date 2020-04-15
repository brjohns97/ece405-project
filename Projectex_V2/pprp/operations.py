import datetime
import threading
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(27, GPIO.IN)

keg_stuff = {
        'start_date_sim': datetime.date(2000,1,1),
        'end_date_sim': datetime.date(2000,1,1),
        'start_time_day': datetime.time(0,0,0),
        'end_time_day': datetime.time(0,0,0),
        'start_datetime_day': datetime.datetime(2020,1,1,0,0,0),	#start datetime of operation using correct start date and start time
        'end_datetime_day': datetime.datetime(2020,1,1,0,0,0),		#end datetime of operation using start date and end time
        'datetime_of_next_pour': datetime.datetime(2020,1,1,0,0,0),
        'drinks': 0,
        'volume': 0,
        'pour_time': 0,
        'time_between_start_of_drinks': 0,
        'time_until_next_pour': 0 ,
        'POURING': 0,
        'START_CHECK': 0,
        
        'test': datetime.datetime(2000,1,1,0,0,0)
}

#volume_of_drink = Q*pour_time	#16 ounces = 0.473176 liters

def start_simulation():
	drink_number = 1
	while(drink_number <= keg_stuff['drinks']):
		threading.Timer(keg_stuff['time_until_next_pour'], pour_drink).start()
		threading.Timer((keg_stuff['time_until_next_pour']+keg_stuff['pour_time']), stop_pour).start()
		
		keg_stuff['time_until_next_pour'] = keg_stuff['time_between_start_of_drinks'] + keg_stuff['time_until_next_pour']
		drink_number = drink_number + 1
	
	

def pour_drink():

	inpt = 27
	pour_time = 0.0
	time_start = 0.0
	time_end = 0.0
	gpio_last = 0
	pulses = 0
	constant = 6.5			#datasheet says 7.5
	total_time = 0.0
	volume = 0.0
	desired_volume = 1.53/4	#in liters

	keg_stuff['datetime_of_next_pour'] = keg_stuff['datetime_of_next_pour'] + datetime.timedelta(seconds=keg_stuff['time_between_start_of_drinks'])


	GPIO.output(18, GPIO.HIGH)
	keg_stuff['POURING']=1
	# while volume < desired_volume:
		# pulses = 0
		# pour_time = 0
		# time_start = time.time()
		# while pulses <=5:
			# gpio_cur = GPIO.input(inpt)
			# if gpio_cur != 0 and gpio_cur != gpio_last:
				# pulses += 1
			# gpio_last = gpio_cur
				

		# time_end = time.time()
		# pour_time = time_end-time_start
		# frequency = pulses/(pour_time)
		# Q = frequency/constant
		# volume = volume + Q*(pour_time/60)
		# total_time = total_time + pour_time

	# GPIO.output(18, GPIO.LOW)
	#keg_stuff['POURING']=0


def set_variables_for_operation():
	keg_stuff['START_CHECK'] = 1

	end_of_day_start_date = datetime.datetime.combine(keg_stuff['start_date_sim'],datetime.time(23,59,59))
	if ((keg_stuff['end_datetime_day']- keg_stuff['start_datetime_day']).total_seconds() > 0):
		time_bar_is_open = (keg_stuff['end_datetime_day'] - keg_stuff['start_datetime_day']).total_seconds()
	else:
		time_bar_is_open = (keg_stuff['end_datetime_day'] + (end_of_day_start_date - keg_stuff['start_datetime_day'])).total_seconds()

	keg_stuff['time_between_start_of_drinks'] = (time_bar_is_open/keg_stuff['drinks'])
	keg_stuff['time_until_next_pour'] = keg_stuff['time_between_start_of_drinks']/2					#initialized to start and end at half of (time between drinks)
	
	keg_stuff['datetime_of_next_pour'] = keg_stuff['start_datetime_day'] + datetime.timedelta(seconds=keg_stuff['time_until_next_pour'])
	
	
def stop_pour():
	GPIO.output(18, GPIO.LOW)
	keg_stuff['POURING']=0





