from flask import Blueprint, render_template, request
from flask_login import current_user
from sqlalchemy import or_
from models import Question, Answer
from services import personalized_feed
from extensions import db

main = Blueprint("main", __name__)

@main.route('/')
def index():
    tab = request.args.get("tab", "personalized")

    if current_user.is_authenticated and tab == "personalized":
        questions = personalized_feed(current_user)
    else:
        if tab == "unanswered":
            questions = (Question.query
                         .filter(~Question.answers.any())
                         .order_by(Question.timestamp.desc())
                         .all()
                         )
        elif tab == "trending":
            questions = (Question.query
                         .outerjoin(Answer)
                         .group_by(Question.id)
                         .order_by(Question.score.desc(), db.func.count(Answer.id).desc())
                         .all()
                         )
        else:
            questions = Question.query.order_by(Question.timestamp.desc()).all()

    return render_template("index.html", questions=questions, tab=tab)

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
