import datetime
import threading
import time
import copy
import math
import RPi.GPIO as GPIO
import routes

GPIO.setmode(GPIO.BCM)
sem = threading.Semaphore()
volume_of_keg = 0;
volume_of_keg_remaining = 0;
datetime_keg_empties = datetime.datetime(2000,1,1,0,0,0);

class Operations:
	def __init__(self,meter_GPIO,valve_GPIO):
		self.pour_time = 0.0
		self.time_start = 0.0
		self.time_end = 0.0
		self.max_pulse = 3
		self.pulse = self.max_pulse
		self.update_flag = 0
		self.constant = 6.8
		self.valve_thread = 0
		self.keg_stuff = {
			'start_date_sim': datetime.date(2000,1,1),
			'end_date_sim': datetime.date(2000,1,1),
			'start_time_day': datetime.time(0,0,0),
			'end_time_day': datetime.time(0,0,0),
			'start_datetime_day': datetime.datetime(2020,1,1,0,0,0),	#start datetime of operation using correct start date and start time
			'end_of_start_datetime_day': datetime.datetime(2020,1,1,0,0,0),		#end datetime of operation using start,yes start, date and end time
			'end_datetime_day': datetime.datetime(2020,1,1,0,0,0),	#end datetime of operation using end date and end time
			'datetime_of_next_pour': datetime.datetime(3000,1,1,12,30),
			'drinks': 0,		#number of drinks poured each day
			'volume_of_drink': 0,	#volume of each drink
			'pour_time': 5,
			'time_between_start_of_drinks': 0,
			'time_until_next_pour': 0,
			'POURING_CHECK': 0,
			'SCHEDULED_CHECK': 0,
			'START_CHECK': 0,
			'drinks_poured': 0,	#total number of drinks poured
			'day': 1,		#what day the simulation is on
			'valve_GPIO': valve_GPIO,
			'meter_GPIO': meter_GPIO,
			'days_of_operation': 0,
			'volume_of_drinks':0,	#volume of drinks poured
			'datetime_logged': datetime.datetime.now()
		}
		GPIO.setup(valve_GPIO, GPIO.OUT, initial=GPIO.LOW)	#valve setup
		GPIO.setup(meter_GPIO, GPIO.IN)				#flow meter setup
		GPIO.add_event_detect(meter_GPIO, GPIO.RISING, callback=self.my_callback)

	    
	def my_callback(self,channel):
	    if (self.pulse == self.max_pulse):
		self.time_end = time.time()
		self.pour_time = self.time_end - self.time_start
		self.time_start = time.time()
		self.update_flag = 1
		self.pulse = 0

	    self.pulse += 1

	def start_simulation(self):
		self.keg_stuff['START_CHECK'] = 1
		self.valve_thread = threading.Timer(self.keg_stuff['time_until_next_pour'], self.pour_drink)
		self.valve_thread.start()


	def pour_drink(self):
	    global sem,volume_of_keg,volume_of_keg_remaining
            sem.acquire()
	    self.pour_time = 0.0
	    self.time_start = 0.0
	    self.time_end = 0.0
	    self.pulse = self.max_pulse
	    self.update_flag = 0
	    self.total_volume = 0
	    Q = 0
	    Q1 = 0
	    Q2 = 0
	    Q3 = 0
	    first_rising_edge = 0
	    desired_volume = self.keg_stuff['volume_of_drink']*0.0295735 #in liters

	    self.keg_stuff['POURING_CHECK']=1
	    pour_start_time = time.time()
	    GPIO.output(self.keg_stuff['valve_GPIO'], GPIO.HIGH)
	    time.sleep(self.keg_stuff['pour_time']) #---> manual pour time code... if uncommented, then comment out entire flow meter calcuation

	    #start of flow meter calculation
	    # while (total_volume < desired_volume):
		# if(self.update_flag == 1 and first_rising_edge != 0):
		    # self.update_flag = 0
		    # frequency = (self.max_pulse)/(self.pour_time)
		    # Q3 = Q2
		    # Q2 = Q1
		    # Q1 = Q
		    # Q = frequency/self.constant
		    # pour_volume = Q*(pour_time/60)
		    # self.keg_stuff['volume_of_drinks'] = self.keg_stuff['volume_of_drinks'] + pour_volume/0.0295735
		    # volume_of_keg_remaining = volume_of_keg - self.keg_stuff['volume_of_drinks']
		    # total_volume = total_volume + pour_volume
		# if(self.update_flag == 1 and first_rising_edge == 0):
		    # self.update_flag = 0
		    # first_rising_edge = 1

	    #end of flow meter calcuation
	    GPIO.output(self.keg_stuff['valve_GPIO'], GPIO.LOW)


	# The code below needs to be here if the flow meter is placed after the valve
	#   timeout = time.time() + 2.5 
	#   while (time.time() < timeout):
	#        if(self.update_flag == 1 and first_rising_edge != 0):
	#            self.update_flag = 0
	#            frequency = (self.max_pulse)/(self.pour_time)
	#            Q3 = Q2
	#            Q2 = Q1
	#            Q1 = Q
	#            Q = frequency/self.constant
	#            #pour_volume = Q*(self.pour_time/60)
	#            #self.keg_stuff['volume_of_drinks'] = self.keg_stuff['volume_of_drinks'] + pour_volume/0.0295735
	#            #volume_of_keg_remaining = volume_of_keg - self.keg_stuff['volume_of_drinks']
	#            total_volume = total_volume + pour_volume

	    pour_end_time = time.time()
	    self.keg_stuff['POURING_CHECK']=0
	    total_pour_time = pour_end_time-pour_start_time
	    self.keg_stuff['drinks_poured'] = self.keg_stuff['drinks_poured'] + 1
	    
	    
	    if(self.keg_stuff['drinks_poured']/self.keg_stuff['drinks']>=self.keg_stuff['day']):
		    self.keg_stuff['time_until_next_pour'] = (24*60*60-self.keg_stuff['time_between_start_of_drinks']*(self.keg_stuff['drinks']-1)) - total_pour_time
		    self.keg_stuff['day'] = self.keg_stuff['day']+1
	    else:
		    self.keg_stuff['time_until_next_pour'] = self.keg_stuff['time_between_start_of_drinks'] - total_pour_time

	    if(self.keg_stuff['day']<=self.keg_stuff['days_of_operation']):
		    self.valve_thread = threading.Timer(self.keg_stuff['time_until_next_pour'], self.pour_drink)
		    self.valve_thread.start()
		    self.keg_stuff['datetime_of_next_pour'] = datetime.datetime.now() + datetime.timedelta(seconds=(self.keg_stuff['time_until_next_pour']))
	    
	    self.keg_stuff['datetime_logged']=datetime.datetime.now()
	    routes.write_csv_files()
	    time.sleep(2.5)
            sem.release()

	def set_variables_for_operation(self):
		global volume_of_keg
		end_of_day_start_datetime = datetime.datetime.combine(self.keg_stuff['start_date_sim'],datetime.time(23,59,59))	#this is the start date with a start time of 12AM slapped onto it
		start_of_day_start_datetime = datetime.datetime.combine(self.keg_stuff['start_date_sim'],datetime.time(0,0,0))	#this is the start date with a start time of 11:59PM slapped onto it
		if ((self.keg_stuff['end_of_start_datetime_day']- self.keg_stuff['start_datetime_day']).total_seconds() > 0):				#example... start time is 5pm end time is 11pm	
			time_bar_is_open = (self.keg_stuff['end_of_start_datetime_day'] - self.keg_stuff['start_datetime_day']).total_seconds()
			self.keg_stuff['days_of_operation'] = (self.keg_stuff['end_date_sim']-self.keg_stuff['start_date_sim']).days+1
		else:																										#example... start time is 5pm, end time is 1am
			time_bar_is_open = (self.keg_stuff['end_of_start_datetime_day']-start_of_day_start_datetime).total_seconds() + (end_of_day_start_datetime - self.keg_stuff['start_datetime_day']).total_seconds()
			self.keg_stuff['days_of_operation'] = (self.keg_stuff['end_date_sim']-self.keg_stuff['start_date_sim']).days

		self.keg_stuff['time_between_start_of_drinks'] = (time_bar_is_open/self.keg_stuff['drinks'])
		self.keg_stuff['time_until_next_pour'] = self.keg_stuff['time_between_start_of_drinks']/2					#initialized to start and end at half of (time between drinks)
		
		self.keg_stuff['datetime_of_next_pour'] = self.keg_stuff['start_datetime_day'] + datetime.timedelta(seconds=self.keg_stuff['time_until_next_pour'])    #datetime of first pour

	def schedule_simulation(self,form):
		global volume_of_keg, volume_of_keg_remaining, sem
		sem.acquire()
		self.keg_stuff['start_date_sim'] =form.start_date_sim.data
		self.keg_stuff['end_date_sim'] =form.end_date_sim.data
		self.keg_stuff['start_time_day'] =form.start_time_day.data
		self.keg_stuff['end_time_day'] =form.end_time_day.data
		self.keg_stuff['drinks'] =form.number_of_drinks.data
		self.keg_stuff['volume_of_drink'] =form.volume_of_drink.data
		if(form.volume_of_keg.data !=0):
			volume_of_keg =form.volume_of_keg.data
			volume_of_keg_remaining =form.volume_of_keg.data
		self.keg_stuff['start_datetime_day'] = datetime.datetime.combine(form.start_date_sim.data,form.start_time_day.data)
		self.keg_stuff['end_of_start_datetime_day'] = datetime.datetime.combine(form.start_date_sim.data,form.end_time_day.data)
		self.keg_stuff['end_datetime_day'] = datetime.datetime.combine(form.end_date_sim.data,form.end_time_day.data)
		self.keg_stuff['SCHEDULED_CHECK'] = 1

		self.reset_variables()
		self.set_variables_for_operation()
		delay = self.keg_stuff['start_datetime_day']-datetime.datetime.now()
		self.valve_thread = threading.Timer(delay.total_seconds(), self.start_simulation)
		self.valve_thread.start()
		sem.release()

	def reset_variables(self):
		self.keg_stuff['START_CHECK'] = 0
		self.keg_stuff['day'] = 1
		self.keg_stuff['drinks_poured'] = 0
		self.keg_stuff['volume_of_drinks'] = 0
		
	def cancel_simulation(self):
		global sem
		sem.acquire()
		if(self.keg_stuff['SCHEDULED_CHECK']==1):
			self.valve_thread.cancel()

		self.keg_stuff['start_date_sim'] = datetime.date(2000,1,1)
		self.keg_stuff['end_date_sim'] = datetime.date(2000,1,1)
		self.keg_stuff['start_time_day'] = datetime.time(0,0,0)
		self.keg_stuff['end_time_day'] = datetime.time(0,0,0)
		self.keg_stuff['start_datetime_day'] = datetime.datetime(2020,1,1,0,0,0)		#start datetime of operation using correct start date and start time
		self.keg_stuff['end_of_start_datetime_day'] = datetime.datetime(2020,1,1,0,0,0)		#end datetime of operation using start,yes start, date and end time
		self.keg_stuff['end_datetime_day'] = datetime.datetime(2020,1,1,0,0,0)			#end datetime of operation using end date and end time
		self.keg_stuff['datetime_of_next_pour'] = datetime.datetime(3000,1,1,12,30)
		self.keg_stuff['drinks'] = 0		#number of drinks poured each day
		self.keg_stuff['volume_of_drink'] = 0	#volume of each drink
		self.keg_stuff['pour_time'] = 5
		self.keg_stuff['time_between_start_of_drinks'] = 0
		self.keg_stuff['time_until_next_pour'] = 0
		self.keg_stuff['POURING_CHECK'] = 0
		self.keg_stuff['SCHEDULED_CHECK'] = 0
		self.keg_stuff['START_CHECK'] = 0
		self.keg_stuff['drinks_poured'] = 0	#total number of drinks poured
		self.keg_stuff['day'] = 1		#what day the simulation is on
		self.keg_stuff['days_of_operation'] = 0
		self.keg_stuff['volume_of_drinks'] = 0	#volume of drinks poured
		self.keg_stuff['datetime_logged'] = datetime.datetime.now()

		sem.release()


def calculate_dtke(valve1,valve2,valve3):
	global volume_of_keg,volume_of_keg_remaining,datetime_keg_empties,sem
	sem.acquire()
	d_volume_of_keg_remaining=copy.deepcopy(volume_of_keg_remaining)
	cummulative_vol = 0;
	
	dvalve1 = copy.deepcopy(valve1.keg_stuff)
	dvalve2 = copy.deepcopy(valve2.keg_stuff)
	dvalve3 = copy.deepcopy(valve3.keg_stuff)
	dvalves = [dvalve1,dvalve2,dvalve3]
	
	current_datetime = datetime.datetime.now();
	previous_datetime = datetime.datetime.now();
	
	while(d_volume_of_keg_remaining>0):
		nearest_pour_datetime = datetime.datetime(3000,1,1,12,30)
		for dvalve in dvalves:
			cummulative_vol = cummulative_vol + dvalve['volume_of_drink']
			if((nearest_pour_datetime>=dvalve['datetime_of_next_pour']) and (dvalve['SCHEDULED_CHECK']==1)):
				nearest_pour_datetime = dvalve['datetime_of_next_pour']
				ddvalve = dvalve	#ddvalve refers to the valve with the nearest pour datetime
		if(cummulative_vol<=0):
			previous_datetime = datetime.datetime(3000,1,1,12,30)
			break
		#after next pour (and valve) is located, pour the drink from that valve (ddvalve)
		previous_datetime = current_datetime
		#poured drink here
		current_datetime = ddvalve['datetime_of_next_pour']
		
		#print (current_datetime.strftime("%Y-%m-%d %H:%M:%S"))
		#print(d_volume_of_keg_remaining)
		d_volume_of_keg_remaining = d_volume_of_keg_remaining-(ddvalve['volume_of_drink'])
		ddvalve['drinks_poured'] = ddvalve['drinks_poured'] + 1
		if(ddvalve['drinks_poured']/ddvalve['drinks']>=ddvalve['day']):
			ddvalve['time_until_next_pour'] = (24*60*60-ddvalve['time_between_start_of_drinks']*(ddvalve['drinks']-1))
			ddvalve['day'] = ddvalve['day']+1
		else:
			ddvalve['time_until_next_pour'] = ddvalve['time_between_start_of_drinks']

		if(ddvalve['day']<=ddvalve['days_of_operation']):
			ddvalve['datetime_of_next_pour'] = current_datetime + datetime.timedelta(seconds=(ddvalve['time_until_next_pour']))
		else: #simulation is done and will not pour again until re-scheduled
			ddvalve['datetime_of_next_pour'] = datetime.datetime(3000,1,1,12,30)

	datetime_keg_empties = previous_datetime
	sem.release()




