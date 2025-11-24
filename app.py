from flask import Flask
from flask_login import LoginManager
from models import User
from extensions import db
from config import Config
from routes import main, auth, qna, vote, user
from models import Question, Answer, Vote, Tag



app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.register_blueprint(main)
app.register_blueprint(auth)
app.register_blueprint(qna)
app.register_blueprint(vote)
app.register_blueprint(user)

@app.context_processor
def inject_sidebar_data():
    user_count = User.query.count()
    question_count = Question.query.count()
    answer_count = Answer.query.count()
    vote_count = Vote.query.count()

    # top 10 tags
    popular_tags = (
        db.session.query(Tag.name)
        .join(Tag.questions)
        .group_by(Tag.id)
        .order_by(db.func.count().desc())
        .limit(10)
        .all()
    )
    popular_tags = [t[0] for t in popular_tags]

    popular_users = (
        db.session.query(User, db.func.count(Answer.id).label("answer_count"))
        .join(Answer, Answer.user_id == User.id)
        .group_by(User.id)
        .order_by(db.desc("answer_count")) # sort by answer count
        .limit(10)
        .all()
    )

    return dict(
        user_count=user_count,
        question_count=question_count,
        answer_count=answer_count,
        vote_count=vote_count,
        popular_tags=popular_tags,
        popular_users=[dict(username=u.username, answer_count=count) for u, count in popular_users]
    )
    
if __name__ == "__main__":
    app.run(debug=True)
