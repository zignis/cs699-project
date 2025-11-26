# Question and answer server for institute members

A web application where users can ask questions, give answers, vote, and tag content for easy search.

# Tech stack

```
$ tree .

├── app.py: application entry point
├── config.py: application configuration, configures the database connnection URL and other parameters
├── create_db.py: creates all the required tables in the database
├── extensions.py: exports the database object
├── forms: contains various HTML forms with validators
│   ├── __init__.py
│   ├── answer.py: form for answering a question
│   ├── login.py: form for logging in a user
│   ├── question.py: form for posting a new question
│   ├── register.py: form for registering a new user
│   └── settings.py: from for modifying user profile
├── main.ipynb: jupyer notebook file to run the project, can also be run directly via CLI
├── models: contains database ORM models, and defines relationships between various models
│   ├── __init__.py
│   ├── answer.py: the answer ORM model
│   ├── question.py: the question ORM model
│   ├── tag.py: the question's tag ORM model
│   ├── user.py: the user ORM model
│   └── vote.py: the vote ORM model
├── requirements.txt: all the required libraries
├── routes: flask blueprints (the REST HTTP endpoints)
│   ├── __init__.py
│   ├── auth.py: the authorization endpoints, exposes routes such as /login, /register, and /logout
│   ├── main.py: the main endpoint, exposes root route (/) and /search
│   ├── qna.py: the question & answer endpoints, exposes /ask, /question, /remove_question/<question_id>, /remove_answer/<answer_id>
│   ├── search_tag.py: the search by tag endpoint, exposes /tag/<tag_name>
│   ├── user.py: the user endpoint, exposes /settings, /profile, /user/<username>
│   └── vote.py: the voting endpoint, exposes /question/<question_id>/<value> and /answer/<answer_id>/<value>
├── services: app services
│   ├── __init__.py
│   ├── recommendation.py: personalized home question feed generation service based on user's past interest
│   └── scraper.py: web-scraping service for finding suggested resources for a given question
├── static: static assets
│   ├── css
│   │   ├── editor.css: stylesheet for markdown editor from https://stackoverflow.design/product/components/editor/#import-via-script-tag
│   │   ├── stacks.css: stylesheet for stacks design system from https://stackoverflow.design/product/develop/using-stacks/#installing
│   │   └── style.css: custom stylesheet
│   ├── default_avatar.png: default user's profile picture
│   ├── user_assets: directory to keep and host all the user uploaded images on the website
│   └── js
│       ├── editor.js: markdown rich text editor script from https://github.com/StackExchange/Stacks-Editor
│       ├── highlight.js: code syntax highlighting library script from https://highlightjs.org
│       └── icons.js: svg icons library from https://github.com/StackExchange/Stacks-Icons
└── templates: jinja HTML templates
    ├── ask.html: ask a new question page
    ├── base.html: base HTML, applies on all routes
    ├── components: reusable components based on jinja macros
    │   ├── avatar.html: user's profile picture macro
    │   └── question_card.html: question display card macro
    ├── index.html: the home page
    ├── login.html: login an existing user page
    ├── profile.html: user's profile page
    ├── register.html: register a new user page
    ├── search_results.html: search for questions by title and body text page
    ├── search_tag.html: search for questions by tag page
    ├── settings.html: user's settings page
    └── view_question.html: display question thread page
```

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

- register or login using the button present in navbar and start using the website by posting questiosn to create threads in which other registered users can post answers.