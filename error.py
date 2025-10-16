from flask import render_template
from helpers import escape

def http_err(message, code=400):
    return render_template("error.html", code=code, message=escape(message)), code
