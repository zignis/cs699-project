from flask import Blueprint, render_template
from models import Question, Tag

tag = Blueprint("tag", __name__)

@tag.route("/tag/<tag_name>")
def search_tag(tag_name):
    tag_name = tag_name.strip()

    results = (
        Question.query
        .join(Question.tags)
        .filter(Tag.name.ilike(f"%{tag_name}%"))
        .order_by(Question.timestamp.desc())
        .all()
    )

    return render_template("search_tag.html", questions=results, q=tag_name)
