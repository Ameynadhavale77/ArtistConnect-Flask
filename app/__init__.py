import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from dotenv import load_dotenv

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)

def create_app():
    load_dotenv()
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret")
    # Force SQLite for this project regardless of environment DATABASE_URL
    db_url = "sqlite:///artistconnect.db"
    # SQLite needs absolute path for flask run from different cwd
    db_path = db_url.replace("sqlite:///", "")
    db_path = os.path.abspath(db_path)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    with app.app_context():
        from . import routes, models
        routes.register_routes(app)
        db.create_all()

    return app