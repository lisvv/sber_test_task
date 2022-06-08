import json
import os

from db import models
from flask import current_app as flask_app
from flask_migrate import Migrate
from sqlalchemy import exists

migrate = Migrate()


def load_fixtures() -> None:
    db = models.db
    db.init_app(flask_app)
    fixtures_dir = flask_app.config.get("FIXTURES_DIR")
    fixtures_path = os.path.join(flask_app.root_path, fixtures_dir)
    fixtures = ("breeds.json", "kitties.json")
    for fixture in fixtures:
        file_path = os.path.join(fixtures_path, fixture)
        file = open(file_path, "r")
        json_instances = json.load(file)
        for json_instance in json_instances:
            model = getattr(models, json_instance.get("model"))
            fields = json_instance.get("fields")
            instance = db.session.query(
                exists().where(model.id == fields.get("id"))
            ).scalar()
            if not instance:
                new_instanace = model(**fields)
                db.session.add(new_instanace)
                db.session.commit()
    db.session.execute(
        "SELECT setval('kitties_id_seq', (SELECT MAX(id) FROM kitties) + 1)"
    )
    db.session.execute(
        "SELECT setval('breeds_id_seq', (SELECT MAX(id) FROM breeds) + 1)"
    )
    db.session.commit()
