from flask import render_template, url_for, flash, redirect, Flask, request, jsonify
from pprp import app
import requests
from pprp.forms import KegeratorForm, MiscForm
import datetime
import operations
import password
import csv
import itertools

import RPi.GPIO as GPIO
import time

password_check = password.password

op1 = operations.Operations(17, 18) #passing in the flow meter GPIO and valve GPIO
op2 = operations.Operations(27, 23) #passing in the flow meter GPIO and valve GPIO
op3 = operations.Operations(22, 24) #passing in the flow meter GPIO and valve GPIO
number_of_valves = 3;
stephens_link = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
brads_link = 'https://www.linkedin.com/in/brad-johnson-684a25149/'
posts = [
    {
        'author': 'Stephen Spade',
        'title': 'Website Created',
        'content': 'Primitive website design has been implemented.',
        'date_posted': 'March 16, 2020',
        'link': stephens_link
    },
    {
        'author': 'Stephen Spade',
        'title': 'LED Lights Up',
        'content': 'An LED connected to the raspberry pi has been successfully been lit up using the website',
        'date_posted': 'March 18, 2020',
        'link': stephens_link
    },
    {
        'author': 'Brad Johnson',
        'title': 'User Input',
        'content': 'The website now successfully takes user input for specifying the parameters for the automation simulation',
        'date_posted': 'April 9, 2020',
        'link': brads_link
    },
    {
        'author': 'Brad Johnson',
        'title': 'Project Code Implemented in Website',
        'content': 'The website now successfully implements the code needed for providing a bar-like environment for the kegerator',
        'date_posted': 'April 11, 2020',
        'link': brads_link
    },
    {
        'author': 'Brad Johnson',
        'title': 'Simulation Statistics',
        'content': 'The website now displays the relevant information regarding the simulation and displays it to the user',
        'date_posted': 'April 16, 2020',
        'link': brads_link
    },
    {
        'author': 'Stephen Spade',
        'title': 'Password Protection & Website Design Update',
        'content': 'Accessing the kegerator controls requires a password to be input & Website has been polished',
        'date_posted': 'April 17, 2020',
        'link': stephens_link
    },
    {
        'author': 'Brad Johnson',
        'title': 'Implement Option for More Valves',
        'content': 'The website now works with 1-3 valves',
        'date_posted': 'May 9, 2020',
        'link': brads_link
    },
    {
        'author': 'Brad Johnson',
        'title': 'Miscellaneous Controls and Simulation Log Added',
        'content': 'Added minor control features and webserver now logs stats after the most recent pour occurs',
        'date_posted': 'May 16, 2020',
        'link': brads_link
    }
]

@app.route("/")

@app.route("/home")
def home():
    return render_template('home.html', posts=posts)

@app.route("/misc", methods=['GET', 'POST'])
def misc():
    global password_check
    form = MiscForm()
    if form.validate_on_submit():
        if(form.valve_1_check_new.data == True):
            op1.cancel_simulation()
        if(form.valve_2_check_new.data == True):
            op2.cancel_simulation()
        if(form.valve_3_check_new.data == True):
            op3.cancel_simulation()
        if(form.volume_of_keg_new.data != None):
            operations.volume_of_keg = form.volume_of_keg_new.data
            operations.volume_of_keg_remaining = form.volume_of_keg_new.data
            
        operations.calculate_dtke(op1,op2,op3);
        flash('Input has been uploaded to Automated Kegerator','success')
        return redirect(url_for('simulation'))
    elif request.method == 'POST':
        if (form.password.data != password_check): #If incorrect password
            flash('ERROR: Incorrect Password','danger')
        if (form.volume_of_keg_new.data <0): #If incorrect password
            flash('ERROR: Keg Volume Must be Positive','danger')
    return render_template('misc.html', form=form)

@app.route("/log")
def log():
    log_values = read_csv_files()
    print(log_values['valve1']['start_datetime_day'])
    print(op1.keg_stuff['start_datetime_day'])
    return render_template('log.html', log_values=log_values)

@app.route("/simulation")
def simulation():
    v1=getStaticValues(op1);
    v2=getStaticValues(op2);
    v3=getStaticValues(op3);
    
    static_values={
        'valve1':v1,
        'valve2':v2,
        'valve3':v3,
        'datetime_keg_empties':operations.datetime_keg_empties,
        'num_of_valves':number_of_valves
    }
    return render_template('sim.html', static_values=static_values)

@app.route("/ac", methods=['GET', 'POST'])
def ac():
    global password_check
    form = KegeratorForm()
    if form.validate_on_submit():
        if(form.valve_1_check.data == True):
            op1.schedule_simulation(form)
        if(form.valve_2_check.data == True):
            op2.schedule_simulation(form)
        if(form.valve_3_check.data == True):
            op3.schedule_simulation(form)

        operations.calculate_dtke(op1,op2,op3);
        flash('Input has been uploaded to Automated Kegerator','success')
        return redirect(url_for('simulation'))
    elif request.method == 'POST':
        if (form.start_date_sim.data>form.end_date_sim.data):
            flash('ERROR: End Date must be after Start Date','danger')
        elif (form.start_date_sim.data==form.end_date_sim.data and form.start_time_day.data>=form.end_time_day.data):
            flash('ERROR: End Date and Time must be after Start Date and Time','danger')
        elif(form.start_date_sim.data<datetime.date.today()):   #if time is impossible relative to todays dates
            flash('ERROR: Start Date must be current day or later','danger')
        elif(form.start_date_sim.data==datetime.date.today() and form.start_time_day.data<=datetime.datetime.now().time()): #if time is impossible relative to todays time and date
            flash('ERROR: Start Date and Time must be current date and time or later','danger')
        elif(form.start_time_day.data==form.end_time_day.data): #if start time of each day is equal to end time of each day
            flash('ERROR: Start and End Times of each day cannot be equal','danger')
        if (form.number_of_drinks.data <= 0):
            flash('ERROR: Invalid Number of Drinks to be Poured','danger')
        if ((form.valve_1_check.data or form.valve_2_check.data or form.valve_3_check.data) == False): #at least 1 valve is checked
            flash('ERROR: At least one valve must be checked','danger')
        if (form.password.data != password_check): #If incorrect password
            flash('ERROR: Incorrect Password','danger')

    return render_template('ac.html', form=form)

@app.route('/_stuff', methods= ['GET'])
def stuff():
    v1=getDynamicValues(op1);
    v2=getDynamicValues(op2);
    v3=getDynamicValues(op3);
    
    dynamic_values={
        'valve1':v1,
        'valve2':v2,
        'valve3':v3,
        'volume_of_keg_remaining':operations.volume_of_keg_remaining,
        'volume_of_keg':operations.volume_of_keg,
        'num_of_valves':number_of_valves
    }
    return jsonify(dynamic_values=dynamic_values)


def getDynamicValues(operation_num):
    valve_num = {
            'POURING_CHECK': operation_num.keg_stuff['POURING_CHECK'],
            'START_CHECK': operation_num.keg_stuff['START_CHECK'],
            'SCHEDULED_CHECK': operation_num.keg_stuff['SCHEDULED_CHECK'],
            'drinks_poured': operation_num.keg_stuff['drinks_poured'],
            'drinks_total': operation_num.keg_stuff['days_of_operation']*operation_num.keg_stuff['drinks'],
            'drinks': operation_num.keg_stuff['drinks'],
            'volume_of_drinks': operation_num.keg_stuff['volume_of_drinks'],
            'volume_of_drink': operation_num.keg_stuff['volume_of_drink'],
            'datetime_of_next_pour': operation_num.keg_stuff['datetime_of_next_pour']
    }
    return valve_num
    
def getStaticValues(operation_num):
    valve_num = {
            'SCHEDULED_CHECK': operation_num.keg_stuff['SCHEDULED_CHECK'],
            'start_datetime_day': operation_num.keg_stuff['start_datetime_day'],
            'end_datetime_day': operation_num.keg_stuff['end_datetime_day'],
            'START_CHECK': operation_num.keg_stuff['START_CHECK'],
    }
    return valve_num
    
def createLogObject():
    valve_num = {
            'SCHEDULED_CHECK': 0,
            'start_datetime_day': 0,
            'end_datetime_day': 0,
            'START_CHECK': 0,
            'POURING_CHECK': 0,
            'START_CHECK': 0,
            'SCHEDULED_CHECK': 0,
            'drinks_poured': 0,
            'drinks': 0,
            'volume_of_drinks': 0,
            'volume_of_drink': 0,
            'datetime_of_next_pour': 0,
            'datetime_logged': datetime.datetime.now(),
            'days_of_operation': 0
    }
    return valve_num

def write_csv_files():
    keg_log_dict = {
        'volume_of_keg_remaining':operations.volume_of_keg_remaining,
        'volume_of_keg':operations.volume_of_keg,
        'num_of_valves':number_of_valves,
        'datetime_keg_empties':operations.datetime_keg_empties
    }
    
    with open('/home/pi/Desktop/Projectex_V2/pprp/static/keg_info.csv', 'w') as csvfile:
        fieldnames = ['volume_of_keg_remaining','volume_of_keg','num_of_valves','datetime_keg_empties']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(keg_log_dict)

    ops = [op1,op2,op3]
    with open('/home/pi/Desktop/Projectex_V2/pprp/static/valve_dicts.csv', 'w') as csvfile:
        fieldnames = ['start_date_sim','end_date_sim','start_time_day','end_time_day','start_datetime_day','end_of_start_datetime_day','end_datetime_day','datetime_of_next_pour','drinks','volume_of_drink','pour_time','time_between_start_of_drinks','time_until_next_pour','POURING_CHECK','SCHEDULED_CHECK','START_CHECK','drinks_poured','day','valve_GPIO','meter_GPIO','days_of_operation','volume_of_drinks','datetime_logged']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for op in ops:
            writer.writerow(op.keg_stuff)


def read_csv_files():
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
            lop['POURING_CHECK'] = row['POURING_CHECK']
            lop['START_CHECK'] = row['START_CHECK']
            lop['SCHEDULED_CHECK'] = row['SCHEDULED_CHECK']
            lop['drinks_poured'] = row['drinks_poured']
            lop['drinks'] = row['drinks']
            lop['volume_of_drinks'] = row['volume_of_drinks']
            lop['volume_of_drink'] = row['volume_of_drink']
            lop['datetime_of_next_pour'] = row['datetime_of_next_pour']
            lop['datetime_logged'] = row['datetime_logged']
            lop['days_of_operation'] = row['days_of_operation']
    
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







