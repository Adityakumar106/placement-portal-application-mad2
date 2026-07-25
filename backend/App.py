from flask import Flask
from flask_cors import CORS
from sqlalchemy import inspect, text
from werkzeug.security import generate_password_hash

from database.database import db
from models.models import User
from mail import init_mail
from flask_caching import Cache
cache = Cache()

app = Flask(__name__)

app.config["CACHE_TYPE"] = "RedisCache"
app.config["CACHE_REDIS_URL"] = "redis://localhost:6379/1"
app.config["CACHE_DEFAULT_TIMEOUT"] = 300




app.config["SECRET_KEY"] = "placement-secret-key"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///placement.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False



db.init_app(app)
cache.init_app(app)
init_mail(app)

CORS(
    app,
    supports_credentials=True,
    origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ]
)



from controllers.authcontroller import *
from controllers.admincontroller import *
from controllers.companycontroller import *
from controllers.studentcontroller import *


def ensure_student_schema():
    inspector = inspect(db.engine)
    columns = {column["name"] for column in inspector.get_columns("student")}

    with app.app_context():
        if "branch" not in columns:
            db.session.execute(text("ALTER TABLE student ADD COLUMN branch VARCHAR(200)"))
        if "cgpa" not in columns:
            db.session.execute(text("ALTER TABLE student ADD COLUMN cgpa VARCHAR(50)"))
        if "phone" not in columns:
            db.session.execute(text("ALTER TABLE student ADD COLUMN phone VARCHAR(50)"))
        db.session.commit()


def ensure_company_schema():
    inspector = inspect(db.engine)
    columns = {column["name"] for column in inspector.get_columns("company")}

    with app.app_context():
        if "rejected" not in columns:
            db.session.execute(text("ALTER TABLE company ADD COLUMN rejected BOOLEAN DEFAULT 0"))
        db.session.commit()


with app.app_context():

    db.create_all()
    ensure_student_schema()
    ensure_company_schema()

    admin = User.query.filter_by(email="admin@gmail.com").first()

    if admin is None:

        admin = User(
            email="admin@gmail.com",
            password=generate_password_hash("admin"),
            role="admin"
        )

        db.session.add(admin)
        db.session.commit()



if __name__ == "__main__":
    app.run(debug=True)
