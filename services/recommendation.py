from models import Question, Answer, Vote, Tag

TAG_WEIGHT = 4
VOTE_WEIGHT = 2
ANSWER_WEIGHT = 1

def get_user_interests(user):
    question_tags = Tag.query.join(Tag.questions).filter(Question.user_id == user.id).all()
    answer_tags = Tag.query.join(Tag.questions).join(Answer).filter(Answer.user_id == user.id).all()
    voted_tags = Tag.query.join(Tag.questions).join(Vote).filter(
        Vote.user_id == user.id, Vote.value == 1
    ).all()
    tags = list(set(question_tags + answer_tags + voted_tags)) # remove duplicates
    return tags

def personalized_feed(user, limit=30):
    interests = get_user_interests(user)
    interest_ids = set(t.id for t in interests)
    questions = Question.query.outerjoin(Answer).group_by(Question.id).all()
    scored = []

    for q in questions:
        score = 0
        shared_tags = []

        for t in q.tags:
            if t.id in interest_ids:
                shared_tags.append(t)

        score += len(shared_tags) * TAG_WEIGHT
        score += q.score * VOTE_WEIGHT
        score += len(q.answers) * ANSWER_WEIGHT
        scored.append((score, q))

    scored.sort(key=lambda x: x[0], reverse=True)
    result = []
    for _, q in scored[:limit]:
        result.append(q)

    return result
