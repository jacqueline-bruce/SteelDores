from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Music(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable = False)
    composer = db.Column(db.String(100), default='')
    genre = db.Column(db.String(30), default='')
    description = db.Column(db.String(2000), default='')
    pdf_link = db.Column(db.String(1000), default='')
    audio_link = db.Column(db.String(1000), default='')
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    is_admin = db.Column(db.Boolean, default=False)
    background_color = db.Column(db.String(7), default='#ffffff')
    drum_color = db.Column(db.String(7), default='#dcdcdc')