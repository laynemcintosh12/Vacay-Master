from flask import Flask, render_template, session, redirect, flash
from other import read_api_key
from models import db, connect_db, User, Destination
from forms import LoginForm, RegisterForm
from sqlalchemy import inspect

app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///vacay-master'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "shhhhh"

connect_db(app)
db.create_all()

secrets_file_path = 'secret.txt'
secret_key = read_api_key(secrets_file_path)



@app.route("/")
def get_homepage():
    """Display common vacation stops with links to more details."""
    
    # Retrieve destination data from the database
    destinations = Destination.query.all()
    
    # Pass the destination data to the template
    return render_template('home.html', destinations=destinations)



@app.route('/route')
def get_destination():
    """display map where you can find your route to destination"""
    secret = secret_key
    return render_template('maps.html', secret=secret)



@app.route('/itin')
def get_itenarary():
    """display table page where you can enter an itenary for select dates"""
    # using table columns as inputs
    # maybe display weather info for dates selected
    # maybe add in a budgeting section
    dates = ["", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    return render_template('itin.html', dates=dates)



@app.route('/blog')
def get_blog():
    """display blog page"""
    # users can comment on places they have visited and mention things to do while there
    return render_template('home.html')



@app.route('/trips')
def get_trips():
    """displays users trips"""
    # trips will be stored where users can view them later on 
    # potentially able to share trip details with others
    return render_template('trips.html')



# Finished Routes ----------------------------------------------------------------------

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Render and Handle user login"""

    if "username" in session:
        return redirect("/")

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)
        if user:
            session['username'] = user.username
            flash(f"Welcome {user.username}!")
            return redirect("/")
        else:
            form.username.errors = ["Invalid username/password"]
            return render_template("/login.html", form=form)

    return render_template("login.html", form=form)



@app.route('/signup', methods=['GET', 'POST'])
def register():
    """register a new user"""

    if "username" in session:
        return redirect("/")
    
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data

        user = User.register(username, password, email)
        db.session.commit()
        session['username'] = user.username
        flash(f"Welcome {user.username}!")
        return redirect("/")

    else:
        return render_template("signup.html", form=form)



@app.route("/logout")
def logout():
    """Logout current user"""

    session.pop("username")
    return redirect("/login")