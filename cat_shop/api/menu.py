from flask import render_template


def index_page() -> str:
    return render_template("index.html")
