from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, FloatField, ValidationError
from wtforms.fields.html5 import DateField, TimeField, DateTimeField
from wtforms.validators import DataRequired, Length, Email, EqualTo
import datetime

def positive_field_check(FlaskForm, field):
	if(field.data) < 0:
		raise ValidationError('Field must be positive')


class RegistrationForm(FlaskForm):
	username 	 = StringField('Username', validators=[DataRequired(), Length(min=5, max=20)])
	email 		 = StringField('Email', validators=[DataRequired(), Email()])
	password 	 = PasswordField('Password',validators=[DataRequired()])
	confirm_password = PasswordField('Confirm_Password',validators=[DataRequired(), EqualTo('password')])
	submit 		 = SubmitField('Sign Up')

class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=5, max=20)])
	password = PasswordField('Password',validators=[DataRequired()])
	remember = BooleanField('Remember Me')
	submit   = SubmitField('Login')

class KegeratorForm(FlaskForm):
	start_date_sim = DateField('Start Date of Simulation',format='%Y-%m-%d', validators=[DataRequired()])
	end_date_sim = DateField('End Date of Simulation',format='%Y-%m-%d', validators=[DataRequired()])
	start_time_day = TimeField('Start Time of Each Day', validators=[DataRequired()])
	end_time_day = TimeField('End Time of Each Day', validators=[DataRequired()])
	number_of_drinks = IntegerField('Number of Drinks to be Poured Each Day', validators=[DataRequired(),positive_field_check])
	volume_of_keg = IntegerField('Starting Volume of Kegerator', validators=[DataRequired()])
	pour_time = FloatField('Pour Time Calibration (time in seconds)', validators=[DataRequired(),positive_field_check])
	test = DateTimeField('Start Date and Time of Simulation')
	submit = SubmitField('Submit')

	def __init__(self, *args, **kwargs):
			FlaskForm.__init__(self, *args, **kwargs)
			self.start_date_sim.data = datetime.date.today()
			self.end_date_sim.data = datetime.date.today()
			self_start_time_day = datetime.datetime.now().time()
			self_end_time_day = datetime.datetime.now().time()
			


	def validate_on_submit(self):
		result = super(KegeratorForm, self).validate()
		if (self.start_date_sim.data>self.end_date_sim.data):	#if dates are impossible relative to the end dates
			return False
		elif(self.start_date_sim.data==self.end_date_sim.data and self.start_time_day.data>=self.end_time_day.data):	#if time is impossible relative to the end time and dates
			return False
		elif(self.start_date_sim.data<datetime.date.today()):	#if time is impossible relative to todays dates
			return False
		elif(self.start_date_sim.data==datetime.date.today() and self.start_time_day.data<=datetime.datetime.now().time()): #if time is impossible relative to todays time and date
			return False
		else:
			return result

