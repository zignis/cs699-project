from flask import Blueprint, abort, redirect, request, url_for
from flask_login import login_required, current_user
from models import Question, Answer, Vote
from extensions import db

vote = Blueprint("vote", __name__)

@vote.post("/question/<int:id>/<value>")
@login_required
def vote_question(id, value):
    try:
        value = int(value)
    except ValueError:
        abort(400)

    if value not in (-1, 1):
        abort(400)

    question = Question.query.get_or_404(id)
    existing = Vote.query.filter_by(user_id=current_user.id, question_id=id).first()

    if not existing:
        db.session.add(Vote(value=value, user_id=current_user.id, question_id=id))
        question.score += value
    else:
        # toggle
        if existing.value == value:
            question.score -= existing.value
            db.session.delete(existing)
        else:
            question.score -= existing.value # remove old vote
            existing.value = value
            question.score += value # add new vote

    db.session.commit()
    return redirect(request.referrer)

#

@vote.post("/answer/<int:id>/<value>")
@login_required
def vote_answer(id, value):
    try:
        value = int(value)
    except ValueError:
        abort(400)

    if value not in (-1, 1):
        abort(400)

    answer = Answer.query.get_or_404(id)
    existing = Vote.query.filter_by(user_id=current_user.id, answer_id=id).first()

    if not existing:
        db.session.add(Vote(value=value, user_id=current_user.id, answer_id=id))
        answer.score += value
    else:
        # toggle
        if existing.value == value:
            answer.score -= existing.value
            db.session.delete(existing)
        else:
            answer.score -= existing.value # remove old vote
            existing.value = value
            answer.score += value # add new vote

    db.session.commit()
    return redirect(request.referrer)

