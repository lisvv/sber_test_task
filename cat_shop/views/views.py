from flask import jsonify, request
from sqlalchemy import func, or_

from db.models import Breed, Kitty


def search():
    return jsonify(x)
