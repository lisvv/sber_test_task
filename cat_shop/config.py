import os


class Config(object):
    APPLICATION_ROOT = "/cat_shop/"
    WORK_DIR = os.path.dirname(os.path.realpath(__file__))
    TESTING = False
    CSRF_ENABLED = True
    # DB_SERVER = "localhost"
    DB_DRIVER = os.environ.get("DB_DRIVER")
    DB_SERVER = os.environ.get("DB_SERVER")
    DB_USER = os.environ.get("DB_USER")
    DB_PASSWORD = os.environ.get("DB_PASSWORD")
    DB_NAME = os.environ.get("DB_NAME")
    MIGRATION_DIRECTORY = os.path.join(f"{WORK_DIR}/db/migrations")
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = os.environ.get("SECRET_KEY")
    ALLOWED_EXTENSIONS = {"apng", "avif", "gif", "jpeg", "png", "svg", "webp"}
    MAX_CONTENT_LENGTH = 5 * 1000 * 1000
    FLASK_ADMIN_SWATCH = "cerulean"
    BABEL_DEFAULT_LOCALE = "ru"
    DEBUG = True
    UPLOAD_FOLDER = "static"
    DEVELOPMENT = True
    FIXTURES_DIR = "fixtures"
    WHOOSHEE_ENABLE_INDEXING = False
    JSON_AS_ASCII = False

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:  # Note: all caps
        return f"{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_SERVER}:5432/{self.DB_NAME}"
