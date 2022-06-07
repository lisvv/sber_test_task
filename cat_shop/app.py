from flask import Flask

from admin.controller import admin, babel
from config import Config
from core import commands
from core.commands import migrate
from db.models import db, ma
from flask_restx import Api
from werkzeug.middleware.proxy_fix import ProxyFix
from api.urls import api
from api.cats import cats_ns
from api.breeds import breed_ns


flask_app = Flask(__name__, instance_relative_config=True)
flask_app.config.from_object(Config())
db.init_app(flask_app)
ma.init_app(flask_app)
api.init_app(flask_app,
             version='1.0',
             title='Cats API',
             description='Cats API for Sber')


api.add_namespace(cats_ns)
api.add_namespace(breed_ns)
babel.init_app(flask_app)
admin.init_app(flask_app)
migrate.init_app(flask_app, db, directory=flask_app.config.get("MIGRATION_DIRECTORY"))
flask_app.cli.command("load-fixtures")(commands.load_fixtures)
flask_app.wsgi_app = ProxyFix(flask_app.wsgi_app)

# # myview = api.CatAPI.as_view("catapi")
#
#
# flask_app.add_url_rule('/cats/', defaults={'cat_id': None},
#                  view_func=myview, methods=['GET', ])
#
# flask_app.add_url_rule('/cats/', view_func=myview, methods=['POST', ])
# flask_app.add_url_rule('/cats/<int:cat_id>', view_func=myview,
#                  methods=['GET', 'PUT', 'DELETE'])


if __name__ == "__main__":
    flask_app.run(host="0.0.0.0", port=3000)
