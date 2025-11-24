from flask import Blueprint, render_template, request, abort
from flask_login import current_user
from sqlalchemy import or_
from models import Question, Answer
from services import personalized_feed
from extensions import db

main = Blueprint("main", __name__)

QUESTIONS_PER_PAGE = 10

@main.route("/")
def index():
    page = request.args.get("page", default=1, type=int)
    tab = request.args.get("tab", default="personalized")

    if page < 1:
        abort(404)

    if current_user.is_authenticated and tab == "personalized":
        questions, total_count = personalized_feed(current_user, page, QUESTIONS_PER_PAGE)

    else:
        if tab == "unanswered":
            base_query = (
                Question.query
                    .filter(~Question.answers.any())
                    .order_by(Question.timestamp.desc())
            )
        elif tab == "trending":
            base_query = (
                Question.query
                    .outerjoin(Answer)
                    .group_by(Question.id)
                    .order_by(Question.score.desc(), db.func.count(Answer.id).desc())
            )
        else:
            base_query = Question.query.order_by(Question.timestamp.desc())

        total_count = base_query.count()
        offset = (page - 1) * QUESTIONS_PER_PAGE
        questions = base_query.offset(offset).limit(QUESTIONS_PER_PAGE).all()

    total_pages = max(1, (total_count + QUESTIONS_PER_PAGE - 1) // QUESTIONS_PER_PAGE)

    if page > total_pages:
        abort(404)

    return render_template(
        "index.html",
        questions=questions,
        tab=tab,
        page=page,
        total_pages=total_pages,
        question_count=total_count,
    )

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
