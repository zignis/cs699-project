from extensions import db

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, nullable=False)  # +1 or -1
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete="CASCADE"), nullable=True)
    answer_id = db.Column(db.Integer, db.ForeignKey('answer.id', ondelete="CASCADE"), nullable=True)
