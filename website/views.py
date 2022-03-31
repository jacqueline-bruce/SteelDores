from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, Music
from . import db
import json

views = Blueprint('views', __name__)

# @views.route('/', methods=['GET', 'POST'])
# @login_required
# def home():
#     if request.method == 'POST':
#         note = request.form.get('note')
#
#         if len(note) < 1:
#             flash('Note is too short!', category='error')
#         else:
#             new_note = Note(data=note, user_id=current_user.id)
#             db.session.add(new_note)
#             db.session.commit()
#             flash('Note added!', category='success')
#
#     return render_template("home.html", user=current_user)

# @views.route('/music-library', methods=['GET', 'POST'])
# @login_required
# def music_library():
#     if request.method == 'POST':
#         music = request.form.get('music')
#         file = request.files['file']

#         if len(music) < 1:
#             flash('Note is too short!', category='error')
#         else:
#             new_music = Music(filename=file.filename, data=file.read(), user_id=current_user.id)
#             db.session.add(new_music)
#             db.session.commit()
#             flash('Music added!', category='success')

#     return render_template("music-library.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route('/delete-music', methods=['POST'])
def delete_music():
    music = json.loads(request.data)
    musicId = music['musicId']
    music = Music.query.get(musicId)
    if music:
        if music.user_id == current_user.id:
            db.session.delete(music)
            db.session.commit()

    return jsonify({})