from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL, Email

class LogInForm(FlaskForm):
    name = StringField("Name Goes Here",validators=[DataRequired("Enter your name.")])
    password = StringField("Password Goes Here:", validators=[DataRequired("Enter your password.")])
    submit = SubmitField("LOG IN")

class RegisterForm(FlaskForm):
    name = StringField("Name Goes Here",validators=[DataRequired("Enter your name.")])
    email = StringField("Email Goes Here:", validators=[DataRequired("Enter your email.")])
    password = StringField("Password Goes Here:", validators=[DataRequired("Enter your password.")])
    submit = SubmitField("SIGN UP")