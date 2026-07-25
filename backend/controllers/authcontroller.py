from flask import request, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from App import app, cache
from database.database import db
from models.models import User, Student, Company

@app.route("/")
def home():
    return jsonify({
        "message": "Placement Portal Backend Running"
    })


@app.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    if not data:
        return jsonify({
            "message": "No data received"
        }), 400

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role")

    if not username or not email or not password or not role:
        return jsonify({
            "message": "All fields are required"
        }), 400

    if role not in ["student", "company"]:
        return jsonify({
            "message": "Invalid role"
        }), 400

    existing = User.query.filter_by(
        email=email
    ).first()

    if existing:
        return jsonify({
            "message": "Email already registered"
        }), 409

    user = User(
        email=email,
        password=generate_password_hash(password),
        role=role
    )

    db.session.add(user)
    db.session.commit()

    if role == "student":

        student = Student(
            user_id=user.id,
            username=username
        )

        db.session.add(student)

    else:

        company = Company(
            user_id=user.id,
            Companyname=username,
            approved=False
        )

        db.session.add(company)

    db.session.commit()
    cache.clear()

    return jsonify({
        "message": "Registration Successful"
    }), 201



@app.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    if not data:
        return jsonify({
            "message": "No data received"
        }), 400

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({
            "message": "Email and Password required"
        }), 400

    user = User.query.filter_by(
        email=email
    ).first()

    if not user:
        return jsonify({
            "message": "User not found"
        }), 404

    if user.blacklisted:
        return jsonify({
            "message": "Your account has been blacklisted."
        }), 403

    if not check_password_hash(user.password, password):
        return jsonify({
            "message": "Invalid password"
        }), 401

    if user.role == "company":

        company = Company.query.filter_by(
            user_id=user.id
        ).first()

        if not company:
            return jsonify({
                "message": "Company account not found",
                "role": "company"
            }), 404

        if company.rejected:
            return jsonify({
                "message": "Company registration has been rejected by admin.",
                "role": "company",
                "approved": False
            }), 403

        if not company.approved:
            return jsonify({
                "message": "Company registration pending admin approval.",
                "role": "company",
                "approved": False
            }), 403

    session["id"] = user.id
    session["role"] = user.role

    return jsonify({

        "message": "Login Successful",
        "role": user.role

    }), 200




@app.route("/logout")
def logout():

    session.clear()

    return jsonify({
        "message": "Logged Out"
    })






