from flask import Blueprint, render_template, request
from sqlalchemy import or_
from models import Question, Answer
from extensions import db

main = Blueprint("main", __name__)

@main.route('/')
def index():
    tab = request.args.get("tab", "newest")
    questions = Question.query.order_by(Question.timestamp.desc()).all()

    if tab == "unanswered":
        questions = (
            Question.query
            .filter(~Question.answers.any())
            .order_by(Question.timestamp.desc())
            .all()
        )
    elif tab == "trending":
        questions = (
            Question.query
            .outerjoin(Answer)
            .group_by(Question.id)
            .order_by(Question.score.desc(), db.func.count(Answer.id).desc())
            .all()
        )

    return render_template('index.html', questions=questions, tab=tab)

#

@main.route("/search")
def search():
    query = request.args.get("q", "").strip()

    if not query:
        return render_template("search_results.html", questions=[], q=query)

    results = (
        Question.query
        .filter(
            or_(
                Question.title.ilike(f"%{query}%"),
                Question.body.ilike(f"%{query}%")
            )
        )
        .order_by(Question.timestamp.desc())
        .all()
    )

    return render_template("search_results.html", questions=results, q=query)
