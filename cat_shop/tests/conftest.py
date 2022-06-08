import pytest

from . import create_app
from .config import Config
from .core.commands import load_fixtures


@pytest.fixture()
def app():
    app = create_app()
    app.config.from_object(Config)
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
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
