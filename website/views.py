from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Note, Folder
from . import db

views = Blueprint('views', __name__) 

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        folder = request.form.get('folder')

        if len(folder) < 1:
            flash('Folder name is too short!', category='error')
        else:
            new_folder = Folder(data=folder, user_id=current_user.id)
            db.session.add(new_folder)
            db.session.commit()
            flash('Folder added!', category='success')
    return render_template("home.html", user=current_user)

@views.route('/folder/<int:id>', methods=['GET', 'POST'])
def folder(id):

    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, folder_id=id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("folder.html", user=current_user, folder = Folder.query.get(id))

@views.route('/notes', methods=['GET', 'POST'])
@login_required
def notes():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("notes.html", user=current_user)

@views.route('/account')
@login_required
def account():
    return render_template("account.html", user=current_user)

@views.route('/delete_note/<int:id>')
def deleteNote(id):
    note_delete = Note.query.get_or_404(id)

    try:
        db.session.delete(note_delete)
        db.session.commit()
        flash('Note deleted!', category='success')
        return redirect(url_for('views.notes'))
    except:
        return "There was a problem deleting."

@views.route('/delete_note_in_folder/<int:id>')
def deleteNoteInFolder(id):
    note_delete = Note.query.get_or_404(id)

    try:
        db.session.delete(note_delete)
        db.session.commit()
        flash('Note deleted!', category='success')
        return redirect(f'/folder/{note_delete.folder_id}')
    except:
        return "There was a problem deleting."

@views.route('/delete_folder/<int:id>')
def deleteFolder(id):
    folder_delete = Folder.query.get_or_404(id)

    try:
        for note in folder_delete.notes:
            db.session.delete(note)
            db.session.commit()

        db.session.delete(folder_delete)
        db.session.commit()
        flash('Folder deleted!', category='success')
        return redirect(url_for('views.home'))
    except:
        return "There was a problem deleting."

@views.route('/delete_account')
def deleteAccount():

    try:
        for note in current_user.notes:
            db.session.delete(note)
            db.session.commit()

        for folder in current_user.folders:
            for note in folder.notes:
                db.session.delete(note)
                db.session.commit()
            db.session.delete(folder)
            db.session.commit()

        db.session.delete(current_user)
        db.session.commit()
        flash('Account deleted!', category='success')
        return redirect(url_for('auth.sign_up'))
    except:
        return "There was a problem deleting."
