from flask import Flask, render_template
from flask_login import LoginManager
from models import db, User
from config import Config
from auth import auth_bp
from questions import qna_bp

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    from models import Question
    questions = Question.query.order_by(Question.timestamp.desc()).all()
    return render_template('index.html', questions=questions)

app.register_blueprint(auth_bp)
app.register_blueprint(qna_bp)
