from flask import render_template, url_for, request, flash, redirect, Flask, request, jsonify
from pprp import app, db#, bcrypt
import requests
from pprp.forms import RegistrationForm, LoginForm, KegeratorForm
from pprp.models import User, Post, Keg
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
        'author': 'Stephen Spade',
        'title': 'Database Implemented',
        'content': 'SQL Database has been implemented and the website is now capable of storing user information',
        'date_posted': 'March 19, 2020'
    },
    {
        'author': 'Stephen Spade',
        'title': 'Project Code Implemented in Website',
        'content': 'The website now successfully implements the code needed for providing a bar-like environment for the kegerator',
        'date_posted': 'tbd'
    },
    {
        'author': 'Stephen Spade',
        'title': 'User Login',
        'content': 'Now users must be logged in to an admin account in order to interact with the kegerator controls.  Users that are not logged in can still view other sections of the website.',
        'date_posted': 'tbd'
    },
    {
        'author': 'Stephen Spade',
        'title': 'About Sections',
        'content': 'The about sections of the website are filled out with relevant information regarding Pint Perfect, the biology research team, and the engineering team. This includes how each party is involved, who is in each group, and what roles they play in the project.',
        'date_posted': 'tbd'
    },
    {
        'author': 'Stephen Spade',
        'title': 'Website hosted on the internet',
        'content': 'Website has been changed from running on a local network to being accessible from anyone on the internet',
        'date_posted': 'tbd'
    }
]

@app.route("/")

@app.route("/home")
def home():
    return render_template('home.html', posts=posts)



@app.route("/led")
def led():
    return render_template('led.html')

@app.route("/led_a1")
def led_a1():
    GPIO.output(18, GPIO.HIGH)
    return render_template('led.html')

@app.route("/led_a2")
def led_a2():
    GPIO.output(18, GPIO.LOW)
    return render_template('led.html')

@app.route("/led_b1")
def led_b1():
    GPIO.output(23, GPIO.HIGH)
    return render_template('led.html')

@app.route("/led_b2")
def led_b2():
    GPIO.output(23, GPIO.LOW)
    return render_template('led.html')

@app.route("/led_c1")
def led_c1():
    GPIO.output(24, GPIO.HIGH)
    return render_template('led.html')

@app.route("/led_c2")
def led_c2():
    GPIO.output(24, GPIO.LOW)
    return render_template('led.html')

@app.route("/make_drink")
def make_drink():
    threading.Timer(0, operations.pour_drink).start()
    return render_template('led.html')



@app.route("/pintperfect")
def pintperfect():
    return render_template('pintperfect.html')

@app.route("/engineering")
def engineering():
    return render_template('engineering.html')

@app.route("/biology")
def biology():
    text = request.args.get('jsdata')

    suggestions_list = ['yeet']

    if text:
        r = requests.get('http://suggestqueries.google.com/complete/search?output=toolbar&hl=ru&q={}&gl=in'.format(text))

        soup = BeautifulSoup(r.content, 'lxml')

        suggestions = soup.find_all('suggestion')

        for suggestion in suggestions:
            suggestions_list.append(suggestion.attrs['data'])

        #print(suggestions_list)

    return render_template('biology.html', suggestions=suggestions_list)
    #data = {'username': 'Pang', 'site': 'stackoverflow.com'}
    #return render_template('biology.html', data=data)
    
@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/Kegerator_Controls")#, methods=['POST'])
def kegcontrol():
    #dim date
    #date = request.form.get("start_date")
    return render_template('kegcontrol.html', **operations.keg_stuff)

@app.route("/keginput", methods=['GET', 'POST'])
def keginput():
    form = KegeratorForm()
    if form.validate_on_submit():
        operations.keg_stuff['start_date_sim'] =form.start_date_sim.data
        operations.keg_stuff['end_date_sim'] =form.end_date_sim.data
        operations.keg_stuff['start_time_day'] =form.start_time_day.data
        operations.keg_stuff['end_time_day'] =form.end_time_day.data
        operations.keg_stuff['drinks'] =form.number_of_drinks.data
        operations.keg_stuff['volume_of_keg'] =form.volume_of_keg.data
        operations.keg_stuff['volume_of_drink'] =form.volume_of_drink.data
        operations.keg_stuff['pour_time'] =form.pour_time.data
        operations.keg_stuff['volume_of_keg_remaining'] =form.volume_of_keg.data
        
        operations.keg_stuff['start_datetime_day'] = datetime.datetime.combine(operations.keg_stuff['start_date_sim'],operations.keg_stuff['start_time_day'])
        operations.keg_stuff['end_of_start_datetime_day'] = datetime.datetime.combine(operations.keg_stuff['start_date_sim'],operations.keg_stuff['end_time_day'])
        operations.keg_stuff['end_datetime_day'] = datetime.datetime.combine(operations.keg_stuff['end_date_sim'],operations.keg_stuff['end_time_day'])

        operations.set_variables_for_operation()

        delay = operations.keg_stuff['start_datetime_day']-datetime.datetime.now()
        threading.Timer(delay.total_seconds(), operations.start_simulation).start()
        
        #keg = Keg(number_of_drinks=form.number_of_drinks.data, number_of_hours=form.number_of_hours.data)
        #db.session.add(keg)
        #db.session.commit()
        flash('Input has been uploaded to Automated Kegerator','success')
        return redirect(url_for('keginput'))
    elif request.method == 'POST':
        if (form.start_date_sim.data>form.end_date_sim.data):
            flash('ERROR: End Date must be after Start Date','danger')
        elif (form.start_date_sim.data==form.end_date_sim.data and form.start_time_day.data>=form.end_time_day.data):
            flash('ERROR: End Date and Time must be after Start Date and Time','danger')
        elif(form.start_date_sim.data<datetime.date.today()):	#if time is impossible relative to todays dates
            flash('ERROR: Start Date must be current day or later','danger')
        elif(form.start_date_sim.data==datetime.date.today() and form.start_time_day.data<=datetime.datetime.now().time()): #if time is impossible relative to todays time and date
            flash('ERROR: Start Date and Time must be current date and time or later','danger')
        if (form.number_of_drinks.data < 0):
            flash('ERROR: Invalid Number of Drinks to be Poured','danger')
        if (form.pour_time.data < 0):
            flash('ERROR: Invalid Pour Time Calibration','danger')

    return render_template('keginput.html', form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        #hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash('Account created for %s! You can now log in'%(form.username.data),'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)



@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == 'admin' and form.password.data == 'admin':
            flash('Logged into Account: %s!'%(form.username.data),'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful', 'danger')
    return render_template('login.html', form=form)


@app.route('/_stuff', methods= ['GET'])
def stuff():
    #var = time.time()
    dynamic_values = {
            'time_until_next_pour': operations.keg_stuff['time_until_next_pour'],
            'POURING': operations.keg_stuff['POURING'],
            'START_CHECK': operations.keg_stuff['START_CHECK'],
            'drinks_poured': operations.keg_stuff['drinks_poured'],
            'day': operations.keg_stuff['day'],
            'volume_of_drinks': operations.keg_stuff['volume_of_drinks'],
            'volume_of_keg_remaining': operations.keg_stuff['volume_of_keg_remaining'],
            'volume_of_keg': operations.keg_stuff['volume_of_keg'],                  # not dynamic but needed for calculations
            'datetime_of_next_pour': operations.keg_stuff['datetime_of_next_pour']
    }
    #time = time.time()
    return jsonify(dynamic_values=dynamic_values)









