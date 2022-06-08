from flask import render_template
from flask_restx import Resource


def index_page():
    x=1
    x=2
    return render_template("index.html")
