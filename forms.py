from wtforms import StringField, PasswordField, DateField, TextAreaField, HiddenField
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



class CreateTripForm(FlaskForm):
    """Create Trip Form"""

    trip_name = StringField(
        'Trip Name',
        validators=[InputRequired()]
        )
    start_date = DateField(
        'Start Date', 
        validators=[InputRequired()]
        )
    end_date = DateField(
        'End Date', 
        validators=[InputRequired()]
        )



class PostForm(FlaskForm):
    """New Post Form"""
    title = StringField(
        'Title', 
        validators=[InputRequired()]
        )
    description = TextAreaField(
        'Description', 
        validators=[InputRequired()]
        )
    

class CommentForm(FlaskForm):
    """New Comment Form"""

    description = TextAreaField(
        'Description', 
        validators=[InputRequired()]
        )