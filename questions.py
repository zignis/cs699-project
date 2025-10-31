from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Question, Tag, Answer
from forms import QuestionForm, AnswerForm

qna_bp = Blueprint('qna', __name__)

@qna_bp.route('/ask', methods=['GET', 'POST'])
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
        flash('Question posted')
        return redirect(url_for('index'))
    return render_template('ask.html', form=form)

@qna_bp.route('/question/<int:id>', methods=['GET', 'POST'])
def view_question(id):
    question = Question.query.get_or_404(id)
    form = AnswerForm()
    if form.validate_on_submit():
        answer = Answer(body=form.body.data, author=current_user, question=question)
        db.session.add(answer)
        db.session.commit()
        flash('Answer posted')
        return redirect(url_for('qna.view_question', id=id))
    return render_template('view_question.html', question=question, form=form)
