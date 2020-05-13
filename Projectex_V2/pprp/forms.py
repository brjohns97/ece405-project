from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, FloatField, ValidationError
from wtforms.fields.html5 import DateField, TimeField, DateTimeField
from wtforms.validators import DataRequired, Length, Email, EqualTo
import datetime

def positive_field_check(FlaskForm, field):
    if(field.data) <= 0:
        raise ValidationError('Field must be positive')

class KegeratorForm(FlaskForm):
    start_date_sim = DateField('Start Date of Simulation',format='%Y-%m-%d', validators=[DataRequired()])
    end_date_sim = DateField('End Date of Simulation',format='%Y-%m-%d', validators=[DataRequired()])
    start_time_day = TimeField('Start Time of Each Day', validators=[DataRequired()])
    end_time_day = TimeField('End Time of Each Day', validators=[DataRequired()])
    number_of_drinks = IntegerField('Number of Drinks to be Poured Each Day', validators=[DataRequired(),positive_field_check])
    volume_of_keg = IntegerField('Starting Volume of Kegerator (volume in oz)', validators=[DataRequired()])
    volume_of_drink = FloatField('Volume of Drink (volume in oz)', validators=[DataRequired(),positive_field_check])
    test = DateTimeField('Start Date and Time of Simulation')
    valve_1_check = BooleanField('Valve 1')
    valve_2_check = BooleanField('Valve 2')
    valve_3_check = BooleanField('Valve 3')
    submit = SubmitField('Submit')
    password = PasswordField('Password',validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
            FlaskForm.__init__(self, *args, **kwargs)
            super(KegeratorForm, self).__init__(*args, **kwargs)
           

    def validate_on_submit(self):
        result = super(KegeratorForm, self).validate()
        if self.password.data != 'dixon': #If incorrect password
            print("wrong password")
            return False
        if ((self.valve_1_check.data or self.valve_2_check.data or self.valve_3_check.data) == False): #if no valves are checked
            print("no valves checked")
            return False
        if (self.start_date_sim.data>self.end_date_sim.data):   #if dates are impossible relative to the end dates
            print("dates are impossible")
            return False
        elif(self.start_date_sim.data==self.end_date_sim.data and self.start_time_day.data>=self.end_time_day.data):    #if time is impossible relative to the end time and dates
            print("time is impossible end tad")
            return False
        elif(self.start_date_sim.data<datetime.date.today()):   #if time is impossible relative to todays dates
            print("dates are impossible rel to tdoay")
            return False
        elif(self.start_date_sim.data==datetime.date.today() and self.start_time_day.data<=datetime.datetime.now().time()): #if time is impossible relative to todays time and date
            print("time is impossible today tad")
            return False
        else:
            return result


    
