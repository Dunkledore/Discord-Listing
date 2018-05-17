import quart.flask_patch
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, URL


class AddGuildForm(FlaskForm):
	description = StringField('guild_description', validators=[DataRequired()])
	admin1_id = StringField('admin1_id')
	admin2_id = StringField('admin2_id')
	invite_link = StringField('invite_link', validators=[URL(), DataRequired()])
	add_guild_submit = SubmitField('add_guild')


class EditGuildForm(FlaskForm):
	description = StringField('guild_description', validators=[DataRequired()])
	admin1_id = StringField('admin1_id')
	admin2_id = StringField('admin2_id')
	invite_link = StringField('invite_link', validators=[URL(), DataRequired()])
	add_guild_submit = SubmitField('add_guild')


class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
	reg_submit = SubmitField('Register')
