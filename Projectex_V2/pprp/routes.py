from flask import render_template, url_for, request, flash, redirect, Flask, request, jsonify
from pprp import app
import requests
from pprp.forms import PassMCForm, PassACForm, KegeratorForm
import datetime
import operations
import threading

import RPi.GPIO as GPIO
import time

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
        'date_posted': 'April ?, 2020'
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
    }
]

@app.route("/")

@app.route("/home")
def home():
    return render_template('home.html', posts=posts)

@app.route("/simulation")
def simulation():
    return render_template('sim.html', **operations.keg_stuff)

@app.route("/ac", methods=['GET', 'POST'])
def ac():
    form = KegeratorForm()
    if form.validate_on_submit():
        operations.reset_variables()
        operations.keg_stuff['start_date_sim'] =form.start_date_sim.data
        operations.keg_stuff['end_date_sim'] =form.end_date_sim.data
        operations.keg_stuff['start_time_day'] =form.start_time_day.data
        operations.keg_stuff['end_time_day'] =form.end_time_day.data
        operations.keg_stuff['drinks'] =form.number_of_drinks.data
        operations.keg_stuff['volume_of_keg'] =form.volume_of_keg.data
        operations.keg_stuff['volume_of_drink'] =form.volume_of_drink.data
        #operations.keg_stuff['pour_time'] =form.pour_time.data
        operations.keg_stuff['volume_of_keg_remaining'] =form.volume_of_keg.data
        
        operations.keg_stuff['start_datetime_day'] = datetime.datetime.combine(operations.keg_stuff['start_date_sim'],operations.keg_stuff['start_time_day'])
        operations.keg_stuff['end_of_start_datetime_day'] = datetime.datetime.combine(operations.keg_stuff['start_date_sim'],operations.keg_stuff['end_time_day'])
        operations.keg_stuff['end_datetime_day'] = datetime.datetime.combine(operations.keg_stuff['end_date_sim'],operations.keg_stuff['end_time_day'])

        operations.set_variables_for_operation()

        delay = operations.keg_stuff['start_datetime_day']-datetime.datetime.now()
        threading.Timer(delay.total_seconds(), operations.start_simulation).start()
        
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
        #if (form.pour_time.data < 0):
         #   flash('ERROR: Invalid Pour Time Calibration','danger')
        if (form.password.data != 'dixon'): #If incorrect password
            flash('ERROR: Incorrect Password','danger')

    return render_template('ac.html', form=form)

@app.route('/_stuff', methods= ['GET'])
def stuff():
    dynamic_values = {
            'time_until_next_pour': operations.keg_stuff['time_until_next_pour'],
            'POURING': operations.keg_stuff['POURING'],
            'START_CHECK': operations.keg_stuff['START_CHECK'],
            'SCHEDULED_CHECK': operations.keg_stuff['SCHEDULED_CHECK'],
            'drinks_poured': operations.keg_stuff['drinks_poured'],
            'day': operations.keg_stuff['day'],
            'volume_of_drinks': operations.keg_stuff['volume_of_drinks'],
            'volume_of_keg_remaining': operations.keg_stuff['volume_of_keg_remaining'],
            'volume_of_keg': operations.keg_stuff['volume_of_keg'],                  # not dynamic but needed for calculations
            'datetime_of_next_pour': operations.keg_stuff['datetime_of_next_pour']
    }
    return jsonify(dynamic_values=dynamic_values)


