from flask import render_template, url_for, request, flash, redirect, Flask, request, jsonify
from pprp import app, db#, bcrypt
import requests
from pprp.forms import RegistrationForm, LoginForm, KegeratorForm, PassMCForm, PassACForm
from pprp.models import User, Post, Keg
import datetime
from pprp import operations
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
    },
    {
        'author': 'tbd',
        'title': 'About the Engineering Team',
        'content': 'The about section for the engineering team has been filled out with some relevant information, such as who is on the team and what roles they play in the project.',
        'date_posted': 'tbd'
    },
    {
        'author': 'tbd',
        'title': 'About the Biology Team',
        'content': 'The about section for the biology team has been filled out with some relevant information, such as who is on the team and what roles they play in the project.',
        'date_posted': 'tbd'
    },
    {
        'author': 'tbd',
        'title': 'About Pint Perfect',
        'content': 'The about section for Pint Perfect has been filled out with some relevant information, such as who Pint Perfect is and what role they play in the project.',
        'date_posted': 'tbd'
    },
    {
        'author': 'tbd',
        'title': 'About the Hardware',
        'content': 'The about section for the hardware has been filled out with some relevant information, such as what hardware was used for the project and what each part does.',
        'date_posted': 'tbd'
    },
    {
        'author': 'tbd',
        'title': 'About the Website',
        'content': 'The about section for the website has been filled out with some relevant information, like how to use it ',
        'date_posted': 'tbd'
    },
    {
        'author': 'tbd',
        'title': 'User Login',
        'content': 'Instead of a static password protected webpage, now users must be logged in to an admin account in order to interact with the kegerator controls.  Users that are not logged in can still view other sections of the website.',
        'date_posted': 'tbd'
    },  
    {
        'author': 'tbd',
        'title': 'Website hosted on the internet',
        'content': 'Website has been changed from running on a local network to being accessible from anyone on the internet',
        'date_posted': 'tbd'
    }
]

@app.route("/")

@app.route("/home")
def home():
    return render_template('home.html', posts=posts)



@app.route("/mc")
def mc():
    return render_template('mc.html')

@app.route("/mc_a_on")
def mc_a_on():
    GPIO.output(18, GPIO.HIGH)
    return render_template('mc.html')

@app.route("/mc_a_off")
def mc_a_off():
    GPIO.output(18, GPIO.LOW)
    return render_template('mc.html')

@app.route("/mc_b_on")
def mc_b_on():
    GPIO.output(23, GPIO.HIGH)
    return render_template('mc.html')

@app.route("/mc_b_off")
def mc_b_off():
    GPIO.output(23, GPIO.LOW)
    return render_template('mc.html')

@app.route("/mc_c_on")
def mc_c_on():
    GPIO.output(24, GPIO.HIGH)
    return render_template('mc.html')

@app.route("/mc_c_off")
def mc_c_off():
    GPIO.output(24, GPIO.LOW)
    return render_template('mc.html')

@app.route("/make_drink")
def make_drink():
    threading.Timer(0, operations.pour_drink).start()
    return render_template('mc.html')



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

@app.route("/simulation")#, methods=['POST'])
def simulation():
    #dim date
    #date = request.form.get("start_date")
    return render_template('sim.html', **operations.keg_stuff)

@app.route("/ac", methods=['GET', 'POST'])
def ac():
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
        elif(form.start_date_sim.data<datetime.date.today()):   #if time is impossible relative to todays dates
            flash('ERROR: Start Date must be current day or later','danger')
        elif(form.start_date_sim.data==datetime.date.today() and form.start_time_day.data<=datetime.datetime.now().time()): #if time is impossible relative to todays time and date
            flash('ERROR: Start Date and Time must be current date and time or later','danger')
        if (form.number_of_drinks.data < 0):
            flash('ERROR: Invalid Number of Drinks to be Poured','danger')
        if (form.pour_time.data < 0):
            flash('ERROR: Invalid Pour Time Calibration','danger')

    return render_template('ac.html', form=form)


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


@app.route("/PassMC", methods=['GET', 'POST'])
def PassMC():
    form = PassMCForm()
    if form.validate_on_submit():
        if form.password.data == 'dixon':
            flash('Correct Password, redirecting...', 'success')
            return redirect(url_for('mc'))
        else:
            flash('Incorrect Password', 'danger')
    return render_template('password_mc.html', form=form)


@app.route("/PassAC", methods=['GET', 'POST'])
def PassAC():
    form = PassACForm()
    if form.validate_on_submit():
        if form.password.data == 'dixon':
            flash('Correct Password, redirecting...', 'success')
            return redirect(url_for('ac'))
        else:
            flash('Incorrect Password', 'danger')
    return render_template('password_ac.html', form=form)

