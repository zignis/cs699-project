import os
import time
import hashlib

from flask import Blueprint, render_template, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from extensions import db
from models import User, Question, Answer, Vote
from forms import UpdateProfileForm

user = Blueprint("user", __name__)

@user.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    form = UpdateProfileForm()

    if form.validate_on_submit():
        changed = False

        # update username
        if form.username.data != current_user.username:
            current_user.username = form.username.data
            changed = True

        # remove avatar
        if form.remove_avatar.data:
            if current_user.avatar:
                old_path = os.path.join(current_app.root_path, "static/user_assets", current_user.avatar)
                if os.path.exists(old_path):
                    os.remove(old_path)
            current_user.avatar = None
            changed = True

        # upload new avatar
        if form.avatar.data:
            file = form.avatar.data
            file_bytes = file.read()
            hashed_name = hashlib.sha256((file.filename + str(time.time())).encode()).hexdigest()[:32]
            ext = secure_filename(file.filename).split(".")[-1]
            filename = f"{hashed_name}.{ext}"
            file_path = os.path.join(current_app.root_path, "static/user_assets", filename)

            with open(file_path, "wb") as f:
                f.write(file_bytes)

            current_user.avatar = filename
            changed = True

        # update passwd
        if form.new_password.data:
            if not check_password_hash(current_user.password, form.current_password.data):
                flash("Incorrect current password", "danger")
                return redirect(url_for("user.settings"))

            current_user.password = generate_password_hash(form.new_password.data)
            changed = True

        if changed:
            db.session.commit()

        flash("Profile updated", "success")
        return redirect(url_for("user.settings"))

    form.username.data = current_user.username
    return render_template("/settings.html", form=form)

#

@user.route('/user/<username>')
def profile(username):
    usr = User.query.filter_by(username=username).first_or_404()
    question_count = Question.query.filter_by(user_id=usr.id).count()
    answer_count = Answer.query.filter_by(user_id=usr.id).count()
    vote_count = Vote.query.filter_by(user_id=usr.id).count()

    return render_template(
        "/profile.html",
        user=usr,
        question_count=question_count,
        answer_count=answer_count,
        vote_count=vote_count
    )

#

@user.route('/profile')
@login_required
def my_profile():
    return redirect(url_for('user.profile', username=current_user.username))
