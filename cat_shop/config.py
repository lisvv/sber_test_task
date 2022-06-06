import os


class Config(object):
    TESTING = False
    CSRF_ENABLED = True
    DB_SERVER = "db"
    DB_USER = os.environ.get("DB_USER")
    DB_PASSWORD = os.environ.get("DB_PASSWORD")
    DB_NAME = os.environ.get("DB_NAME")
    DB_DRIVER = os.environ.get("DB_DRIVER")
    DB_PORT = os.environ.get("DB_PORT")
    MIGRATION_DIRECTORY = os.path.join("db/migrations")
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = os.environ.get("SECRET_KEY")
    ALLOWED_EXTENSIONS = {"apng", "avif", "gif", "jpeg", "png", "svg", "webp"}
    MAX_CONTENT_LENGTH = 5 * 1000 * 1000
    FLASK_ADMIN_SWATCH = "cerulean"
    BABEL_DEFAULT_LOCALE = "ru"
    DEBUG = True
    # HOST_NAME_PORT = "127.0.0.1:3000"
    DEVELOPMENT = True
    FIXTURES_DIR = "fixtures"
    WHOOSHEE_ENABLE_INDEXING = False

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:  # Note: all caps
        return f"{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_SERVER}/{self.DB_NAME}"
