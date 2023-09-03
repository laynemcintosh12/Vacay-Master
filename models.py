from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    db.app = app
    db.init_app(app)



class User(db.Model):
    """User model."""
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    email = db.Column(db.String)

    trips = db.relationship('Trips', backref='user')
    comments = db.relationship('Comments', backref='user')

    @classmethod
    def register(cls, username, password, email):
        """Register a user and encrypt their password"""
        hashed = bcrypt.generate_password_hash(password).decode('utf-8')
        user = cls(username=username, password=hashed, email=email)
        db.session.add(user)
        return user
    
    @classmethod
    def authenticate(cls, username, password):
        """Check if user exists and authenticate with password"""
        user = cls.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False



class Trips(db.Model):
    """Trips model."""
    __tablename__ = "trips"

    trip_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    destination_id = db.Column(db.Integer, db.ForeignKey('destinations.dest_id'))
    iten_id = db.Column(db.Integer, db.ForeignKey('itineraries.iten_id'))



class Destination(db.Model):
    """Destination model."""
    __tablename__ = "destinations"

    dest_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.comment_id'))



class Itinerary(db.Model):
    """Itinerary model."""
    __tablename__ = "itineraries"

    iten_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dates = db.Column(db.String)
    comments = db.Column(db.String, nullable=True)
    budget = db.Column(db.Integer, nullable=True)



class Comments(db.Model):
    """Comments model."""
    __tablename__ = "comments"

    comment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    destination_id = db.Column(db.Integer, db.ForeignKey('destinations.dest_id'))



class UsersTrips(db.Model):
    """Mapping of users to trips."""
    __tablename__ = "users_trips"

    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.trip_id'), primary_key=True)



class UsersComments(db.Model):
    """Mapping of users to comments."""
    __tablename__ = "users_comments"

    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.comment_id'), primary_key=True)
