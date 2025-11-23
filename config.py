import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "__DEVELOPMENT_SECRET__")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "postgresql://postgres:pg_pass@localhost:5432/qna"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
