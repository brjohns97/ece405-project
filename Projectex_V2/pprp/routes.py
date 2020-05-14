from flask import render_template, url_for, flash, redirect, Flask, request, jsonify
from pprp import app
import requests
from pprp.forms import KegeratorForm
import datetime
import operations

import RPi.GPIO as GPIO
import time

op1 = operations.Operations(17, 18) #passing in the flow meter GPIO and valve GPIO
op2 = operations.Operations(27, 23) #passing in the flow meter GPIO and valve GPIO
op3 = operations.Operations(22, 24) #passing in the flow meter GPIO and valve GPIO
number_of_valves = 3;
posts = [
    {
        'author': 'Stephen Spade',
        'title': 'Website Created',
        'content': 'Primitive website design has been implemented.',
        'date_posted': 'March 16, 2020'
    },
    {
        'author': 'Stephen Spade',
        'title': 'LED Lights Up',
        'content': 'An LED connected to the raspberry pi has been successfully been lit up using the website',
        'date_posted': 'March 18, 2020'
    },
    {
        'author': 'Brad Johnson',
        'title': 'User Input',
        'content': 'The website now successfully takes user input for specifying the parameters for the automation simulation',
        'date_posted': 'April 9, 2020'
    },
    {
        'author': 'Brad Johnson',
        'title': 'Project Code Implemented in Website',
        'content': 'The website now successfully implements the code needed for providing a bar-like environment for the kegerator',
        'date_posted': 'April 11, 2020'
    },
    {
        'author': 'Brad Johnson',
        'title': 'Simulation Statistics',
        'content': 'The website now displays the relevant information regarding the simulation and displays it to the user',
        'date_posted': 'April 16, 2020'
    },
    {
        'author': 'Stephen Spade',
        'title': 'Password Protection & Website Design Update',
        'content': 'Accessing the kegerator controls requires a password to be input & Website has been polished',
        'date_posted': 'April 17, 2020'
    },
    {
        'author': 'Brad Johnson',
        'title': 'Created option to use 1-3 valves',
        'content': 'The website now works with 3 valves',
        'date_posted': 'May 9, 2020'
    }
]

@app.route("/")

@app.route("/home")
def home():
    return render_template('home.html', posts=posts)

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
    form = KegeratorForm()
    if form.validate_on_submit():
        print("valid submission")
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
            print form.valve_1_check.data
            print form.valve_2_check.data
            print form.valve_3_check.data
            flash('ERROR: At least one valve must be checked','danger')
        if (form.password.data != 'dixon'): #If incorrect password
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
            'time_until_next_pour': operation_num.keg_stuff['time_until_next_pour'],
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





