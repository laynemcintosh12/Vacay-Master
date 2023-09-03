from wtforms import StringField, PasswordField, IntegerField
from wtforms.validators import InputRequired, Length, Email
from flask_wtf import FlaskForm


class LoginForm(FlaskForm):
    """Login form"""

    username = StringField(
        "Username",
        validators=[InputRequired(), Length(min=1, max=20)],
    )
    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(min=6, max=55)],
    )


class RegisterForm(FlaskForm):
    """Registration Form"""

    username = StringField(
        "Username",
        validators=[InputRequired(), Length(min=1, max=20)],
    )
    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(min=6, max=55)],
    )
    email = StringField(
        "Email",
        validators=[InputRequired(), Email(), Length(max=50)],
    )
"""     address = StringField(
        "Address",
        validators=[InputRequired(), Length(max=30)],
    )
    phone = IntegerField(
        "Phone Number",
        validators=[InputRequired(), Length(min=9, max=11)],
    ) """
