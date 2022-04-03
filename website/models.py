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
    date = db.Column(db.Date, default=func.current_date())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    def set_title(self, new_title):
        self.title = new_title
        db.session.add(self)
        db.session.commit()


    def set_composer(self, new_composer):
        self.composer = new_composer
        db.session.add(self)
        db.session.commit()


    def set_genre(self, new_genre):
        self.genre = new_genre
        db.session.add(self)
        db.session.commit()


    def set_description(self, new_description):
        self.description = new_description
        db.session.add(self)
        db.session.commit()


    def set_pdf(self, new_pdf):
        self.pdf_link = new_pdf
        db.session.add(self)
        db.session.commit()


    def set_audio(self, new_audio):
        self.audio_link = new_audio
        db.session.add(self)
        db.session.commit()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    first_name = db.Column(db.String(150))
    password = db.Column(db.String(150))
    is_admin = db.Column(db.Boolean, default=False)
    background_color = db.Column(db.String(7), default='#000000')
    drum_color = db.Column(db.String(7), default='#e4a33a')
    sign_up_date = db.Column(db.Date(), default=func.current_date())


    def set_email(self, new_email):
        self.email = new_email
        db.session.add(self)
        db.session.commit()


    def set_password(self, new_password):
        self.password = new_password
        db.session.add(self)
        db.session.commit()


    def set_first_name(self, new_first_name):
        self.first_name = new_first_name
        db.session.add(self)
        db.session.commit()


    def set_is_admin(self, new_is_admin):
        self.is_admin = new_is_admin
        db.session.add(self)
        db.session.commit()


    def set_background(self, new_background):
        self.background_color = new_background
        db.session.add(self)
        db.session.commit()


    def set_drum_color(self, new_drum_color):
        self.drum_color = new_drum_color
        db.session.add(self)
        db.session.commit()