from models import Question, Answer, Vote, Tag

TAG_WEIGHT = 4
VOTE_WEIGHT = 2
ANSWER_WEIGHT = 1

def get_user_interests(user):
    question_tags = Tag.query.join(Tag.questions).filter(Question.user_id == user.id)
    answer_tags = Tag.query.join(Tag.questions).join(Answer).filter(Answer.user_id == user.id)
    voted_tags = Tag.query.join(Tag.questions).join(Vote).filter(
        Vote.user_id == user.id, Vote.value == 1
    )
    tags = set(question_tags.union(answer_tags).union(voted_tags).all())
    return [t.id for t in tags]

def personalized_feed(user, page, per_page):
    interest_ids = set(get_user_interests(user))
    base_query = (
        Question.query.outerjoin(Answer)
            .group_by(Question.id)
            .order_by(Question.timestamp.desc())
    )

    total_count = base_query.count()
    batch = base_query.limit(300).all() # limited scoring window

    scored = []

    for q in batch:
        score = 0
        shared_tags = [t for t in q.tags if t.id in interest_ids]
        score += len(shared_tags) * TAG_WEIGHT
        score += q.score * VOTE_WEIGHT
        score += len(q.answers) * ANSWER_WEIGHT
        scored.append((score, q))

    scored.sort(key=lambda x: x[0], reverse=True)

    start = (page - 1) * per_page
    end = start + per_page
    paginated_questions = [q for _, q in scored[start:end]]

    return paginated_questions, total_count
