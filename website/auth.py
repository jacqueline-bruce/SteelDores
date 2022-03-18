from flask import Blueprint, render_template, request, flash, redirect, url_for, send_file
from .models import User
from io import BytesIO
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/lead')
@login_required
def nav_to_lead():
    return render_template("lead.html", user=current_user)

@auth.route('/double-tenor')
@login_required
def nav_to_double_tenor():
    return render_template("double-tenor.html", user=current_user)

@auth.route('/double-second')
@login_required
def nav_to_double_second():
    return render_template("double-second.html", user=current_user)

@auth.route('/guitar-cello')
@login_required
def nav_to_guitar_cello():
    return render_template("guitar-cello.html", user=current_user)

@auth.route('/tenor-bass')
@login_required
def nav_to_tenor_bass():
    return render_template("tenor-bass.html", user=current_user)

@auth.route('/six-bass')
@login_required
def nav_to_six_bass():
    return render_template("six-bass.html", user=current_user)

@auth.route('/help')
@login_required
def nav_to_help():
    return render_template("help.html", user=current_user)

@auth.route('/settings')
@login_required
def nav_to_settings():
    return render_template("settings.html", user=current_user)

@auth.route('/menu')
@login_required
def nav_to_menu():
    return render_template("menu.html", user=current_user)

@auth.route('/drum-select')
@login_required
def nav_to_drum_select():
    return render_template("drum-select.html", user=current_user)

#@auth.route('/music-library')
#@login_required
#def nav_to_music_library():
#    return render_template("music-library.html", user=current_user)

@auth.route('/add-music')
@login_required
def nav_to_add_music():
    return render_template("add-music.html", user=current_user)

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)