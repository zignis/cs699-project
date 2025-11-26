# Question and answer server for institute members

A web application where users can ask questions, give answers, vote, and tag content for easy search.

# Tech stack

- Backend: Python, Flask
- Frontend: HTML + CSS (based on [Stacks](https://stackoverflow.design/) design system)
- Data models and routes in `models/` and `routes/` folders
- Static assets in `static/`, HTML templates in `templates/`
- Setup tools: `create_db.py`, `config.py`, `extensions.py`
- Dependencies listed in `requirements.txt`

# Running

- install dependencies:
```shell
pip install -r requirements.txt
```

- setup a PostgreSQL database instance, create a database named as `qna`, and provide its connection URL in `config.py`.
- make changes as needed in `config.py`
  
- create tables:
```shell
python create_db.py
```

- run the app:
```shell
python app.py
```
