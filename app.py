from flask import Flask, render_template, request
from other import read_api_key
app = Flask(__name__)
app.app_context().push()

secrets_file_path = 'secrets.txt'
secret_key = read_api_key(secrets_file_path)


@app.route("/")
def get_homepage():
    """display common vacation stops with links to more details"""
    #links can go to travel websites
    return render_template('home.html')


@app.route('/route')
def get_destination():
    """display map where you can find your route to destination"""
    secret = secret_key
    return render_template('maps.html', secret=secret)


@app.route('/iten')
def get_itenarary():
    """display table page where you can enter an itenary for select dates"""
    # using table columns as inputs
    # maybe display weather info for dates selected
    # maybe add in a budgeting section
    return render_template('iten.html')


@app.route('/blog')
def get_blog():
    """display blog page"""
    # users can comment on places they have visited and mention things to do while there
    return render_template('home.html')


@app.route('/login')
def get_login():
    return render_template('home.html')


@app.route('/signup')
def signup():
    return render_template('home.html')


@app.route('/trips')
def get_trips():
    """displays users trips"""
    # trips will be stored where users can view them later on 
    # potentially able to share trip details with others
    return render_template('home.html')