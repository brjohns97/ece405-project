import datetime
import threading
import time
import math
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
        'end_of_start_datetime_day': datetime.datetime(2020,1,1,0,0,0),		#end datetime of operation using start,yes start, date and end time
        'end_datetime_day': datetime.datetime(2020,1,1,0,0,0),	#end datetime of operation using end date and end time
        'datetime_of_next_pour': datetime.datetime(2020,1,1,0,0,0),
        'drinks': 0,
        'volume_of_keg': 0,
        'volume_of_drink': 0,
        'pour_time': 0,
        'time_between_start_of_drinks': 0,
        'time_until_next_pour': 0 ,
        'POURING': 0,
        'SCHEDULED_CHECK': 0,
        'START_CHECK': 0,
        'drinks_poured': 0,
        'day': 1,
        'days_of_operation': 0,
        'volume_of_drinks':0,
        'volume_of_keg_remaining': 0,
        'datetime_keg_empties': datetime.datetime(2000,1,1,0,0,0),
        'test': datetime.datetime(2000,1,1,0,0,0)
}

def start_simulation():
	keg_stuff['START_CHECK'] = 1
	threading.Timer(keg_stuff['time_until_next_pour'], pour_drink).start()


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
	desired_volume = keg_stuff['volume_of_drink']*0.0295735	#in liters


	keg_stuff['POURING']=1
	pour_start_time = time.time()
	GPIO.output(18, GPIO.HIGH)
	# time.sleep(keg_stuff['pour_time']) #---> manual pour time code... if uncommented, then comment out entire flow meter calcuation
	
	#start of flow meter calculation
	while volume < desired_volume:
		pulses = 0
		pour_time = 0
		time_start = time.time()
		while pulses <=5:
			gpio_cur = GPIO.input(inpt)
			if gpio_cur != 0 and gpio_cur != gpio_last:
				pulses += 1
			gpio_last = gpio_cur
				

		time_end = time.time()
		pour_time = time_end-time_start
		frequency = pulses/(pour_time)
		Q = frequency/constant
		volume = volume + Q*(pour_time/60)
		total_time = total_time + pour_time
	#end of flow meter calcuation
	GPIO.output(18, GPIO.LOW)
	pour_end_time = time.time()
	keg_stuff['POURING']=0
	
	total_pour_time = pour_end_time-pour_start_time
	keg_stuff['volume_of_drinks'] = keg_stuff['volume_of_drinks'] + volume/0.0295735
	keg_stuff['volume_of_keg_remaining'] = keg_stuff['volume_of_keg'] - keg_stuff['volume_of_drinks']
	
	keg_stuff['drinks_poured'] = keg_stuff['drinks_poured'] + 1

	if(keg_stuff['drinks_poured']/keg_stuff['drinks']>=keg_stuff['day']):
		keg_stuff['time_until_next_pour'] = keg_stuff['time_between_start_of_drinks'] + 24*60*60 - total_pour_time
		keg_stuff['day'] = keg_stuff['day']+1

	else:
		keg_stuff['time_until_next_pour'] = keg_stuff['time_between_start_of_drinks'] - total_pour_time

	if(keg_stuff['day']<=keg_stuff['days_of_operation']):
		threading.Timer(keg_stuff['time_until_next_pour'], pour_drink).start()
		keg_stuff['datetime_of_next_pour'] = datetime.datetime.now() + datetime.timedelta(seconds=(keg_stuff['time_until_next_pour']))
	#else:
		##reset_variables() #dont reset variables here, do it at the beginnning of submit validation


def set_variables_for_operation():
	keg_stuff['SCHEDULED_CHECK'] = 1

	end_of_day_start_datetime = datetime.datetime.combine(keg_stuff['start_date_sim'],datetime.time(23,59,59))	#this is the start date with a start time of 12AM slapped onto it
	start_of_day_start_datetime = datetime.datetime.combine(keg_stuff['start_date_sim'],datetime.time(0,0,0))	#this is the start date with a start time of 11:59PM slapped onto it
	if ((keg_stuff['end_of_start_datetime_day']- keg_stuff['start_datetime_day']).total_seconds() > 0):				#example... start time is 5pm end time is 11pm	
		time_bar_is_open = (keg_stuff['end_of_start_datetime_day'] - keg_stuff['start_datetime_day']).total_seconds()
		keg_stuff['days_of_operation'] = (keg_stuff['end_date_sim']-keg_stuff['start_date_sim']).days+1
	else:																										#example... start time is 5pm, end time is 1am
		time_bar_is_open = (keg_stuff['end_of_start_datetime_day']-start_of_day_start_datetime).total_seconds() + (end_of_day_start_datetime - keg_stuff['start_datetime_day']).total_seconds()
		keg_stuff['days_of_operation'] = (keg_stuff['end_date_sim']-keg_stuff['start_date_sim']).days

	keg_stuff['time_between_start_of_drinks'] = (time_bar_is_open/keg_stuff['drinks'])
	keg_stuff['time_until_next_pour'] = keg_stuff['time_between_start_of_drinks']/2					#initialized to start and end at half of (time between drinks)
	
	keg_stuff['datetime_of_next_pour'] = keg_stuff['start_datetime_day'] + datetime.timedelta(seconds=keg_stuff['time_until_next_pour'])    #datetime of first pour
	
	drinks_until_keg_empties = math.ceil(keg_stuff['volume_of_keg']/keg_stuff['volume_of_drink'])
	day_keg_will_empty = math.floor((drinks_until_keg_empties-1)/(keg_stuff['drinks']))
	drink_number_keg_will_empty = ((drinks_until_keg_empties/(keg_stuff['drinks']))-day_keg_will_empty)*(keg_stuff['drinks'])
	keg_stuff['datetime_keg_empties'] = keg_stuff['datetime_of_next_pour']+datetime.timedelta(days=day_keg_will_empty, seconds=(keg_stuff['time_between_start_of_drinks']*(drink_number_keg_will_empty-1)))


def stop_pour():
	GPIO.output(18, GPIO.LOW)
	keg_stuff['POURING']=0

def reset_variables():
	keg_stuff['start_date_sim'] = datetime.date(2000,1,1)
        keg_stuff['end_date_sim'] = datetime.date(2000,1,1)
        keg_stuff['start_time_day'] = datetime.time(0,0,0)
        keg_stuff['end_time_day'] = datetime.time(0,0,0)
        keg_stuff['start_datetime_day'] = datetime.datetime(2020,1,1,0,0,0)	#start datetime of operation using correct start date and start time
        keg_stuff['end_of_start_datetime_day'] = datetime.datetime(2020,1,1,0,0,0)		#end datetime of operation using start,yes start, date and end time
        keg_stuff['end_datetime_day'] = datetime.datetime(2020,1,1,0,0,0)	#end datetime of operation using end date and end time
        keg_stuff['datetime_of_next_pour'] = datetime.datetime(2020,1,1,0,0,0)
        keg_stuff['drinks'] = 0
        keg_stuff['volume_of_keg'] = 0
        keg_stuff['volume_of_drink'] = 0
        keg_stuff['pour_time'] = 0
        keg_stuff['time_between_start_of_drinks'] = 0
        keg_stuff['time_until_next_pour'] = 0 
        keg_stuff['POURING'] = 0
        keg_stuff['SCHEDULED_CHECK'] = 0
        keg_stuff['START_CHECK'] = 0
        keg_stuff['drinks_poured'] = 0
        keg_stuff['day'] = 1
        keg_stuff['days_of_operation'] = 0
        keg_stuff['volume_of_drinks'] = 0
        keg_stuff['volume_of_keg_remaining'] = 0
        keg_stuff['datetime_keg_empties'] = datetime.datetime(2000,1,1,0,0,0)
        keg_stuff['test'] = datetime.datetime(2000,1,1,0,0,0)




