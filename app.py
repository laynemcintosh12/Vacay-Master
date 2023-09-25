from flask import Flask, render_template, session, redirect, flash, request, jsonify
from other import read_api_key
from models import db, connect_db, User, Destination, Post, Comment, Itinerary, Trip
from forms import LoginForm, RegisterForm, CreateTripForm, PostForm, CommentForm
from functions import generate_dates_between, get_itin
from datetime import datetime

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


""" Issues:
If a user is logged out, they might be able to still see the home-logged.html
Users might be able to delete other users posts
Itinerary is saving properly however when a user clicks to see their itin from a past trip it doesnt autofill
Dates must be saved under the trip_id instead of stored in the session ********************************************* NECESSARY
"""




@app.route('/login', methods=['GET', 'POST'])
def login():
    """Render and Handle user login"""

    # if user is logged in, redirect to home page
    if "username" in session:
        return redirect("/dest")

    form = LoginForm()
    if form.validate_on_submit():
        # get form data
        username = form.username.data
        password = form.password.data

        # authenticate user
        user = User.authenticate(username, password)

        if user:
            # add username to session, flash welcome message, redirect to home page
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

    # if user is logged in, redirect to home page
    if "username" in session:
        return redirect("/")
    
    form = RegisterForm()
    if form.validate_on_submit():
        # get form data
        username = form.username.data
        password = form.password.data
        email = form.email.data

        # add user to database
        user = User.register(username, password, email)
        db.session.commit()

        # add username to session, flash welcome message, redirect to home page
        session['username'] = user.username
        flash(f"Welcome {user.username}!")
        return redirect("/")
    else:
        return render_template("signup.html", form=form)



@app.route("/logout")
def logout():
    """Logout current user"""

    session.pop("username")
    return redirect("/")



@app.route("/", methods=["GET", "POST"])
def get_homepage():
    """Renders Home Page"""

    # Check if the user is logged in
    if "username" in session:
        form = CreateTripForm()

        # If user is logged in, display home-logged.html with form on starting first trip
        if form.validate_on_submit():
            name = form.trip_name.data
            start_date = form.start_date.data 
            end_date = form.end_date.data  

            # Get the user's username from the session
            username = session.get('username')

            # Query the database to find the user by username
            user = User.query.filter_by(username=username).first()
            if user:
                user_id = user.user_id

                # Add new trip to the database
                new_trip = Trip(user_id=user_id, name=name)
                db.session.add(new_trip)
                db.session.commit()
                
                # Save start_date and end_date to the session
                session['trip_id'] = new_trip.trip_id
                session['start_date'] = start_date.strftime('%Y-%m-%d')
                session['end_date'] = end_date.strftime('%Y-%m-%d')

                # If user completes the form, redirect the user to destinations page
                return redirect('/dest') 
        # if user is logged in
        return render_template('home-logged.html', form=form)
    
    # if user is not logged in 
    return render_template('home.html')


### DESTINATIONS ROUTES ------------------------------------------------------------------------------

@app.route('/dest')
def get_destinations():
    """Display common vacation stops with links to more details."""
    
    destinations = Destination.query.all()
    return render_template('destinations.html', destinations=destinations)


@app.route('/blog/<int:dest_id>', methods=['GET', 'POST'])
def get_blog(dest_id):
    """Display blog page and handle form submission"""

    # Get destination from ID
    destination = Destination.query.get(dest_id)  

    if destination:
        # Get specific posts based on dest_id
        posts = Post.query.filter_by(dest_id=dest_id).all()

        # Query comments for all posts
        comments = Comment.query.filter(Comment.post_id.in_([post.post_id for post in posts])).all()

        if request.method == 'POST':
            # handle user locking in their trip destination
            session['dest_id'] = dest_id
            trip_id = session.get('trip_id')
            trip = Trip.query.get(trip_id)
            trip.dest_id = destination.dest_id
            return redirect(f'/itin/{trip_id}')

        return render_template('posts.html', destination=destination, posts=posts, comments=comments)
    else:
        return redirect('/home')

    


@app.route('/newpost/<int:dest_id>', methods=['GET', 'POST'])
def new_post(dest_id):
    """Create a new post"""
    form = PostForm()

    if form.validate_on_submit():
        # If the form has been submitted and is valid
        title = form.title.data
        description = form.description.data

        # Create a new post and add it to the database
        new_post = Post(title=title, description=description, dest_id=dest_id)
        db.session.add(new_post)
        db.session.commit()
        return redirect(f'/blog/{dest_id}')  # Redirect to the blog page for the destination

    return render_template('newpost.html', form=form)


@app.route('/newcomment/<int:post_id>', methods=['GET', 'POST'])
def new_comment(post_id):
    """Create a new comment for a post"""
    form = CommentForm()

    if form.validate_on_submit():
        # If the form has been submitted and is valid
        description = form.description.data

        # Get the user's username from the session
        username = session.get('username')

        # Query the database to find the user by username
        user = User.query.filter_by(username=username).first()

        if user:
            user_id = user.user_id

            # Create a new comment and add it to the database
            new_comment = Comment(description=description, post_id=post_id, user_id=user_id)
            db.session.add(new_comment)
            db.session.commit()

            # Get the specific post in order to backreference the dest_id and pass into redirect
            post = Post.query.get(post_id)
            dest_id = post.post_destination.dest_id
            return redirect(f'/blog/{dest_id}')  
        
    return render_template('newcomment.html', form=form)



@app.route('/delete_post/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    if request.method == 'POST':
        # Query the database to find the post by post_id
        post = Post.query.get(post_id)

        if post:
            # Check if the logged-in user owns this post
            username = session.get('username')
            user = User.query.filter_by(username=username).first()

            if user and post.user_id == user.user_id:
                # Delete the post and commit the changes to the database
                db.session.delete(post)
                db.session.commit()
                flash("Post deleted successfully")
            else:
                flash("You do not have permission to delete this post")
        else:
            flash("Post not found")

        # Redirect back to the blog page for the destination of the deleted post
        return redirect(f'/blog/{post.dest_id}')

    return jsonify({"message": "Invalid request"})



#### ITINERARY ROUTES ---------------------------

@app.route('/itin/<int:trip_id>')
def get_itinerary(trip_id):
    """Display table page where you can enter an itinerary for select dates"""

    # Retrieve the selected dates from the session as strings
    start_date_str = session.get('start_date')
    end_date_str = session.get('end_date')

    # Convert the date strings to Python datetime objects
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

    # Fetch the user's itinerary for the given trip
    username = session.get('username')
    user = User.query.filter_by(username=username).first()

    if user:
        user_id = user.user_id

        # Fetch the itinerary based on user_id, trip_id, and date
        itinerary_data = Itinerary.query.filter_by(user_id=user_id, trip_id=trip_id).all()
        print(user_id)
        print(trip_id)
        print(itinerary_data)
        itin = get_itin(itinerary_data)
        
        trip = Trip.query.get(trip_id)

        dates = generate_dates_between(start_date, end_date)
        return render_template('itin.html', dates=dates, trip=trip, itinerary_data=itin)

    return render_template('itin.html', dates=[], trip=None, itinerary_data={})





@app.route('/save_itinerary', methods=['POST'])
def save_itinerary():
    if request.method == 'POST':
        # Retrieve data sent from the JavaScript code
        print('something happend')
        data = request.json  # Use request.json to access JSON data
        val = data.get('val')
        hour = data.get('time')
        date = data.get('date')
        username = session.get('username')
        user = User.query.filter_by(username=username).first()
        print(val)
        print(hour)
        print(date)
        if user:
            user_id = user.user_id
            trip_id = session.get('trip_id')

            # Create a new Itinerary and add it to the database
            itinerary = Itinerary(user_id=user_id, trip_id=trip_id, date=date, hour=hour, val=val)
            db.session.add(itinerary)
            db.session.commit()

            # Add itinerary to the trip 
            trip = Trip.query.get(trip_id)
            trip.itin_id = itinerary.itin_id
            

        return jsonify({"message": "Data saved successfully"})

    return jsonify({"message": "Invalid request"})



#### GOOGLE MAPS ROUTE --------------------------------------------------------------------------------

@app.route('/route')
def get_map():
    """display map where you can find your route to destination"""

    # get api key
    secret = secret_key

    # get destination
    dest_id = session.get('dest_id')
    destination = Destination.query.get(dest_id)
    return render_template('maps.html', secret=secret, destination=destination)


#### USERS TRIPS ROUTE -----------------------------------------------------------------


@app.route('/trips')
def my_trips():
    # Query the database to retrieve the user's trips
    username = session.get('username') 
    user = User.query.filter_by(username=username).first()
    trips = Trip.query.filter_by(user_id=user.user_id).all()

    return render_template('trips.html', trips=trips)


@app.route('/remove_trip/<int:trip_id>', methods=['POST'])
def remove_trip(trip_id):
    if request.method == 'POST':
        # Query the database to find the trip by trip_id
        trip = Trip.query.get(trip_id)

        if trip:
            # Check if the logged-in user owns this trip
            username = session.get('username')
            user = User.query.filter_by(username=username).first()

            if user and trip.user_id == user.user_id:
                # Delete the trip and commit the changes to the database
                db.session.delete(trip)
                db.session.commit()
                flash("Trip removed successfully")
            else:
                flash("You do not have permission to remove this trip")
        else:
            flash("Trip not found")

        # Redirect back to the /trips route
        return redirect('/trips')

    return jsonify({"message": "Invalid request"})
