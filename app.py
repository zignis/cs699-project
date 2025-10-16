from flask import Flask, redirect, render_template, request
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from error import http_err

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # todo
        return redirect("/")
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # todo
        return redirect("/login")
    else:
        return render_template("register.html")

def errorhandler(e):
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return http_err(e.name, e.code)

for code in default_exceptions:
    app.errorhandler(code)(errorhandler)