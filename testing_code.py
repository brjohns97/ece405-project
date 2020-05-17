import threading, time
import flowclass
import copy
import RPi.GPIO as GPIO
import csv
import itertools

#GPIO.setmode(GPIO.BCM)
#GPIO.setup(18, GPIO.OUT, initial=GPIO.LOW)	#valve 1
#GPIO.setup(23, GPIO.OUT, initial=GPIO.LOW)	#valve 2
#GPIO.setup(24, GPIO.OUT, initial=GPIO.LOW)	#valve 3

def modify_drink_num(f,drink_number):
    df = copy.deepcopy(f.keg_stats)
    print('pour_check: ' + str(df['pour_check']))
    return

def make_csv_file():
    global f1, f2, f3
    fs = [f1,f2,f3]
    with open('/home/pi/Desktop/valve_dics.csv', 'r+') as csvfile:
        fieldnames = f1.keg_stats.keys()
        #fieldnames = ['pour_check', 'start_check', 'valve_number', 'drinks', 'datetime_of_next_pour']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for objectf in fs:
            writer.writerow(objectf.keg_stats)

f1 = flowclass.FlowCalculation(1)
f2 = flowclass.FlowCalculation(2)
f3 = flowclass.FlowCalculation(3)


#f1.scheduleSimulation()
#f2.scheduleSimulation()
#f3.scheduleSimulation()
#make_csv_file(fs)
#f1.set_drink_num(20)

#f1.keg_stats['drinks'] = 15
#print('num of drikns: '+str(f1.keg_stats['drinks']))
#f1.write_to_csv()
#f2.keg_stats['drinks'] = 20
#f2.write_to_csv()
# for f in fs:
    # ff = f
    # print(f.valve_num)

#modify_drink_num(f1,20)
# ff.drink_num = 20
# print(f1.drink_num)
# print(f2.drink_num)
# print(f3.drink_num)
# print(ff.drink_num))
def createLogObject():
    valve_num = {
            'SCHEDULED_CHECK': 0,
            'start_datetime_day': 0,
            'end_datetime_day': 0,
            'START_CHECK': 0,
            'time_until_next_pour': 0,
            'POURING_CHECK': 0,
            'START_CHECK': 0,
            'SCHEDULED_CHECK': 0,
            'drinks_poured': 0,
            #'drinks_total': operation_num.keg_stuff['days_of_operation']*operation_num.keg_stuff['drinks'],
            'drinks': 0,
            'volume_of_drinks': 0,
            'volume_of_drink': 0,
            'datetime_of_next_pour': 0
    }
    return valve_num

def read_csv_file():
    lop1 = createLogObject()
    lop2 = createLogObject()
    lop3 = createLogObject()
    lops = [lop1,lop2,lop3]
    with open('/home/pi/Desktop/Projectex_V2/pprp/static/valve_dicts.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for (row,lop) in itertools.izip_longest(reader,lops):
            lop['SCHEDULED_CHECK'] = row['SCHEDULED_CHECK']
            lop['start_datetime_day'] = row['start_datetime_day']
            lop['end_datetime_day'] = row['end_datetime_day']
            lop['START_CHECK'] = row['START_CHECK']
            lop['time_until_next_pour'] = row['time_until_next_pour']
            lop['POURING_CHECK'] = row['POURING_CHECK']
            lop['START_CHECK'] = row['START_CHECK']
            lop['SCHEDULED_CHECK'] = row['SCHEDULED_CHECK']
            lop['drinks_poured'] = row['drinks_poured']
            lop['drinks'] = row['drinks']
            lop['volume_of_drinks'] = row['volume_of_drinks']
            lop['volume_of_drink'] = row['volume_of_drink']
            lop['datetime_of_next_pour'] = row['datetime_of_next_pour']
    
    keg_log_dict = {
        'volume_of_keg_remaining':0,
        'volume_of_keg':0,
        'num_of_valves':0,
        'datetime_keg_empties':0
    }
    
    with open('/home/pi/Desktop/Projectex_V2/pprp/static/keg_info.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            keg_log_dict['volume_of_keg_remaining'] = row['volume_of_keg_remaining']
            keg_log_dict['volume_of_keg'] = row['volume_of_keg']
            keg_log_dict['num_of_valves'] = row['num_of_valves']
            keg_log_dict['datetime_keg_empties'] = row['datetime_keg_empties']

    return_dictionary = {
        'valve1':lops[0],
        'valve2':lops[1],
        'valve3':lops[2],
        'volume_of_keg_remaining':keg_log_dict['volume_of_keg_remaining'],
        'volume_of_keg':keg_log_dict['volume_of_keg'],
        'num_of_valves':keg_log_dict['num_of_valves'],
        'datetime_keg_empties':keg_log_dict['datetime_keg_empties']
    }
    
    return return_dictionary

newdict = read_csv_file()
print(newdict['valve1']['SCHEDULED_CHECK'])

var = 1
#while var!= 0:
#    var = input("Enter something: ")
#    print(f1.keg_stats.keys())
    #print(threading.active_count())
    #if(var == 1):
    #    f1.cancel_valve()
    #if(var == 2):
    #    f2.cancel_valve()
    #if(var == 3):
    #    f3.cancel_valve()
    


