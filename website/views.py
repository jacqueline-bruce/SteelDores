from flask import Blueprint, redirect, render_template, request, flash, jsonify, url_for
from flask_login import login_required, current_user
from .models import Music
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/music-library')
@login_required
def nav_to_music_library():
    query = db.session.query(Music)
    return render_template("music-library.html", user=current_user, query=query)


@views.route('/delete/<int:id>', methods=['GET'])
def delete_music(id):
    music = Music.query.get(id)
    if music:
        db.session.delete(music)
        db.session.commit()
        flash('Sample deleted successfully!', category='success')

    query = db.session.query(Music)
    return redirect(url_for('views.nav_to_music_library'))