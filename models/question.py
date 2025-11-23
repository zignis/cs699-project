from datetime import datetime
from extensions import db
from .tag import question_tags

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    body = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    score = db.Column(db.Integer, default=0, nullable=False)
    view_count = db.Column(db.Integer, default=0, nullable=False)

    tags = db.relationship('Tag', secondary=question_tags, backref=db.backref('questions', lazy='dynamic'), cascade="all")
    answers = db.relationship('Answer', backref='question', cascade="all, delete-orphan", passive_deletes=True, lazy=True)
    votes = db.relationship('Vote', backref='question', cascade="all, delete-orphan", passive_deletes=True, lazy=True)