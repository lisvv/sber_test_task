from flask import Flask

from admin.controller import admin, babel
from config import Config
from core import commands
from core.commands import migrate
from db.models import db
from views import views

flask_app = Flask(__name__, instance_relative_config=True)
flask_app.config.from_object(Config())
db.init_app(flask_app)
babel.init_app(flask_app)
admin.init_app(flask_app)
migrate.init_app(flask_app, db, directory=flask_app.config.get("MIGRATION_DIRECTORY"))
flask_app.route("/search")(views.search)
flask_app.cli.command("load-fixtures")(commands.load_fixtures)


if __name__ == "__main__":
    flask_app.run(host="0.0.0.0", port=3000)
