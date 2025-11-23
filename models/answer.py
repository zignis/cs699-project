from datetime import datetime
from extensions import db

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    score = db.Column(db.Integer, default=0, nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete="CASCADE"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)

    votes = db.relationship('Vote', backref='answer', cascade="all, delete-orphan", passive_deletes=True, lazy=True)