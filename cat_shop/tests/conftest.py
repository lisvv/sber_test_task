import pytest
from config import TestConfig
from core.commands import load_fixtures
from flask.testing import FlaskClient, FlaskCliRunner
from cat_shop import create_app


@pytest.fixture()
def app():
    app = create_app()
    app.config.from_object(TestConfig)
    app.config.update(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "postgresql://test_user:password@localhost/test_db",
        }
    )
    with app.app_context():
        load_fixtures()

    yield app


@pytest.fixture()
def client(app) -> FlaskClient:
    return app.test_client()


@pytest.fixture()
def runner(app) -> FlaskCliRunner:
    return app.test_cli_runner()
