from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'artist' or 'organizer'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    artist_profile = db.relationship('ArtistProfile', backref='user', uselist=False)
    organizer_profile = db.relationship('OrganizerProfile', backref='user', uselist=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class ArtistProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category = db.Column(db.String(80), nullable=False)  # Singer, DJ, Dancer...
    location = db.Column(db.String(120), nullable=False)
    bio = db.Column(db.Text, nullable=True)
    demo_links = db.Column(db.Text, nullable=True)  # newline separated links
    charges = db.Column(db.String(80), nullable=True)  # optional text
    profile_image = db.Column(db.String(200), nullable=True)  # filename for profile image

class OrganizerProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    organization = db.Column(db.String(150), nullable=True)

class BookingRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # artist user_id
    organizer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # organizer user_id
    event_date = db.Column(db.String(40), nullable=False)
    venue = db.Column(db.String(200), nullable=False)
    budget = db.Column(db.String(80), nullable=True)
    message = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default="pending")  # pending/accepted/rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)