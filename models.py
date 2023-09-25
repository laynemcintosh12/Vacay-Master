from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    db.app = app
    db.init_app(app)



class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    email = db.Column(db.String, unique=True)

    trips = db.relationship('Trip', backref='user')
    comments = db.relationship('Comment', backref='user')

    @classmethod
    def register(cls, username, password, email):
        hashed = bcrypt.generate_password_hash(password).decode('utf-8')
        user = cls(username=username, password=hashed, email=email)
        db.session.add(user)
        return user
    
    @classmethod
    def authenticate(cls, username, password):
        user = cls.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return None



class Trip(db.Model):
    __tablename__ = "trips"

    trip_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    name = db.Column(db.String)
    dest_id = db.Column(db.Integer, db.ForeignKey('destinations.dest_id'), nullable=True)
    itin_id = db.Column(db.Integer, db.ForeignKey('itineraries.itin_id'), nullable=True)



class Itinerary(db.Model):
    __tablename__ = "itineraries"

    itin_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.trip_id'))
    date = db.Column(db.String)
    hour = db.Column(db.Integer)
    val = db.Column(db.String)



class Comment(db.Model):
    __tablename__ = "comments"

    comment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id'))
    description = db.Column(db.String)



class Destination(db.Model):
    __tablename__ = "destinations"

    dest_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    description = db.Column(db.String)

    posts = db.relationship('Post', back_populates='destination')



class Post(db.Model):
    __tablename__ = "posts"

    post_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dest_id = db.Column(db.Integer, db.ForeignKey('destinations.dest_id'))
    title = db.Column(db.String)
    description = db.Column(db.String)

    destination = db.relationship('Destination', back_populates='posts')
