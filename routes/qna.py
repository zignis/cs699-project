from flask import Blueprint, render_template, redirect, url_for, flash, abort, session, request
from flask_login import login_required, current_user
from models import Question, Tag, Answer
from extensions import db
from forms import QuestionForm, AnswerForm
from services import aggregated_search

qna = Blueprint('qna', __name__)

@qna.route('/ask', methods=['GET', 'POST'])
@login_required
def ask():
    form = QuestionForm()
    if form.validate_on_submit():
        question = Question(title=form.title.data, body=form.body.data, author=current_user)
        tag_names = [t.strip().lower() for t in form.tags.data.split(',') if t.strip()]
        for name in tag_names:
            tag = Tag.query.filter_by(name=name).first()
            if not tag:
                tag = Tag(name=name)
                db.session.add(tag)
            question.tags.append(tag)
        db.session.add(question)
        db.session.commit()
        flash('Question posted', 'success')
        return redirect(url_for('main.index'))
    return render_template('ask.html', form=form)

#

@qna.route('/question/<int:id>', methods=['GET', 'POST'])
def view_question(id):
    question = Question.query.get_or_404(id)
    tab = request.args.get("tab", "votes")
    form = AnswerForm()

    if tab == "newest":
        answers = Answer.query.filter_by(question_id=id).order_by(Answer.timestamp.desc()).all()
    else:
        answers = Answer.query.filter_by(question_id=id).order_by(Answer.score.desc()).all() # most voted

    if form.validate_on_submit():
        answer = Answer(body=form.body.data, author=current_user, question=question)
        db.session.add(answer)
        db.session.commit()
        flash('Answer posted', 'success')
        return redirect(url_for('qna.view_question', id=id))

    viewed_key = f"viewed_question::{id}"
    if not session.get(viewed_key):
        question.view_count += 1
        db.session.commit()
        session[viewed_key] = True

    suggested_resources = aggregated_search(question.title)

    return render_template('view_question.html', question=question, answers=answers, suggested_resources=suggested_resources, form=form, tab=tab)

#

@qna.post("/remove_question/<int:id>")
@login_required
def delete_question(id):
    question = Question.query.get_or_404(id)
    if question.user_id != current_user.id:
        abort(403)

    db.session.delete(question)
    db.session.commit()
    flash("Question deleted", "success")
    return redirect(url_for("main.index"))

#

@qna.post("/answer/<int:answer_id>")
@login_required
def delete_answer(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    if answer.user_id != current_user.id:
        abort(403)

    question_id = answer.question_id
    db.session.delete(answer)
    db.session.commit()
    flash("Answer deleted", "success")
    return redirect(url_for("qna.view_question", id=question_id))