from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

from admin.controller import admin, babel
from api.breeds import breed_ns
from api.cats import cats_ns
from api.menu import index_page
from api.urls import api
from config import Config
from core import commands
from core.commands import migrate
from db.models import db, ma


def create_app():
    flask_app = Flask(__name__, instance_relative_config=True)
    flask_app.config.from_object(Config())

    db.init_app(flask_app)
    ma.init_app(flask_app)
    flask_app.route('/')(index_page)
    api.init_app(
        flask_app, version="1.0", title="Cats API", description="Cats API for Sber", doc='/docs'
    )
    babel.init_app(flask_app)
    admin.init_app(flask_app)
    migrate.init_app(
        flask_app, db, directory=flask_app.config.get("MIGRATION_DIRECTORY")
    )

    flask_app.cli.command("load-fixtures")(commands.load_fixtures)

    flask_app.wsgi_app = ProxyFix(flask_app.wsgi_app)


    api.add_namespace(cats_ns)
    api.add_namespace(breed_ns)


    return flask_app

application = create_app()