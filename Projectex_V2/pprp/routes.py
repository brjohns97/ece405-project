from flask import render_template, url_for, request, flash, redirect, Flask, request, jsonify
from pprp import app
import requests
from pprp.forms import PassMCForm, PassACForm, KegeratorForm
import datetime
import operations
import threading

import RPi.GPIO as GPIO
import time

op1 = operations.Operations(17) #passing in the flow meter GPIO
op1.keg_stuff['valve_GPIO']=18
                        
op2 = operations.Operations(27) #passing in the flow meter GPIO
op2.keg_stuff['valve_GPIO']=23

op3 = operations.Operations(22) #passing in the flow meter GPIO
op3.keg_stuff['valve_GPIO']=24

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
        'content': 'The website now works with a maximum of 3 valves',
        'date_posted': 'May 8, 2020'
    }
]

@app.route("/")

@app.route("/home")
def home():
    return render_template('home.html', posts=posts)

@app.route("/simulation")
def simulation():
    return render_template('sim.html', **op1.keg_stuff)

@app.route("/ac", methods=['GET', 'POST'])
def ac():
    form = KegeratorForm()
    if form.validate_on_submit():
        if(form.valve_1_check.data == True):
            op1.schedule_simulation(form)
        if(form.valve_2_check.data == True):
            op2.schedule_simulation(form)
        if(form.valve_3_check.data == True):
            op3.schedule_simulation(form)
            
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
        if (form.number_of_drinks.data < 0):
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
    dynamic_values = {
            'time_until_next_pour': op1.keg_stuff['time_until_next_pour'],
            'POURING': op1.keg_stuff['POURING'],
            'START_CHECK': op1.keg_stuff['START_CHECK'],
            'SCHEDULED_CHECK': op1.keg_stuff['SCHEDULED_CHECK'],
            'drinks_poured': op1.keg_stuff['drinks_poured'],
            'day': op1.keg_stuff['day'],
            'volume_of_drinks': op1.keg_stuff['volume_of_drinks'],
            'volume_of_keg_remaining': op1.keg_stuff['volume_of_keg_remaining'],
            'volume_of_keg': op1.keg_stuff['volume_of_keg'],                  # not dynamic but needed for calculations
            'datetime_of_next_pour': op1.keg_stuff['datetime_of_next_pour']
    }
    return jsonify(dynamic_values=dynamic_values)


