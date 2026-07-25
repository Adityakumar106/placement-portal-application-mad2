from flask import request, session,jsonify,send_file
from App import app
from database.database import db
from App import cache
from models.models import Student, Company, Drive, Application , Interview, ExportJob
from flask import send_from_directory
import os

from celery.result import AsyncResult


def get_cache_key(prefix: str):
    user_id = session.get("id")
    role = session.get("role")
    return f"{prefix}:{role}:{user_id}"


def format_date(value):
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    try:
        return value.strftime("%Y-%m-%d")
    except Exception:
        return str(value)

@app.route("/student/dashboard", methods=["GET"])
def student_dashboard():

    if session.get("role") != "student":
        return jsonify({"message": "Unauthorized"}), 401

    cache_key = get_cache_key("student_dashboard")
    cached = cache.get(cache_key)
    if cached is not None:
        return jsonify(cached)

    drives = Drive.query.filter_by(status="open").all()

    result = []

    for drive in drives:

        company = Company.query.get(drive.company_id)

        result.append({

            "id": drive.id,
            "company": company.Companyname if company else "",
            "title": drive.title,
            "job_title": drive.job_title,
            "eligibility": drive.eligibility,
            "deadline": format_date(drive.deadline)

        })
    payload = {
        "drives": result
    }
    cache.set(cache_key, payload, timeout=300)
    return jsonify(payload)

@app.route("/student/profile", methods=["GET"])
def student_profile():

    if session.get("role") != "student":
        return jsonify({"message": "Unauthorized"}), 401

    cache_key = get_cache_key("student_profile")
    cached = cache.get(cache_key)
    if cached is not None:
        return jsonify(cached)

    student = Student.query.filter_by(user_id=session["id"]).first()

    if student is None:
        return jsonify({"message": "Student not found"}), 404
    payload = {
        "username": student.username,
        "degree": student.degree,
        "course": student.course,
        "branch": student.branch,
        "cgpa": student.cgpa,
        "phone": student.phone,
        "linkdin": student.linkdin,
        "resume": student.resume,
        "about": student.about
    }
    cache.set(cache_key, payload, timeout=300)
    return jsonify(payload)

@app.route("/student/profile", methods=["PUT"])
def update_student_profile():

    if session.get("role") != "student":
        return jsonify({"message": "Unauthorized"}), 401

    student = Student.query.filter_by(user_id=session["id"]).first()

    if student is None:
        return jsonify({"message": "Student not found"}), 404

    data = request.get_json()

    student.username = data.get("username")
    student.degree = data.get("degree")
    student.course = data.get("course")
    student.branch = data.get("branch")
    student.cgpa = data.get("cgpa")
    student.phone = data.get("phone")
    student.linkdin = data.get("linkdin")
    student.resume = data.get("resume")
    student.about = data.get("about")

    db.session.commit()
    cache.clear()

    return jsonify({
        "message": "Profile updated successfully"
    })

@app.route("/student/drive/<int:id>")
def student_drive_details(id):

    if session.get("role")!="student":
        return jsonify({"message":"Unauthorized"}),401

    cache_key = get_cache_key(f"student_drive_{id}")
    cached = cache.get(cache_key)
    if cached is not None:
        return jsonify(cached)

    student=Student.query.filter_by(user_id=session["id"]).first()

    drive=Drive.query.get_or_404(id)

    company=Company.query.get(drive.company_id)

    application=Application.query.filter_by(
        student_id=student.id,
        drive_id=id
    ).first()
    payload = {

        "id":drive.id,
        "title":drive.title,
        "company":company.Companyname if company else "",
        "job_title":drive.job_title,
        "description":drive.description,
        "eligibility":drive.eligibility,
        "salary":drive.salary,
        "deadline":format_date(drive.deadline),
        "status":drive.status,
        "applied":application is not None

    }
    cache.set(cache_key, payload, timeout=300)
    return jsonify(payload)



@app.route("/student/apply/<int:id>", methods=["POST"])
def apply_drive(id):

    if session.get("role") != "student":
        return jsonify({"message": "Unauthorized"}), 401

    student = Student.query.filter_by(
        user_id=session["id"]
    ).first()

    if student is None:
        return jsonify({"message": "Student not found"}), 404

    drive = Drive.query.get(id)

    if drive is None:
        return jsonify({"message": "Drive not found"}), 404

    if drive.status != "open":
        return jsonify({"message": "Drive is closed"}), 400

    # Check if already applied
    existing = Application.query.filter_by(
        student_id=student.id,
        drive_id=id,
        company_id=drive.company_id
    ).first()

    if existing:
        return jsonify({
            "message": "You have already applied for this drive."
        }), 400

    application = Application(
        student_id=student.id,
        drive_id=id,
        company_id=drive.company_id,
        status="Applied"
    )

    db.session.add(application)
    db.session.commit()
    cache.clear()

    return jsonify({
        "message": "Application submitted successfully."
    }), 201

from flask import jsonify, session

@app.route("/student/applications")
def student_applications():

    if session.get("role") != "student":
        return jsonify({"message": "Unauthorized"}), 401

    cache_key = get_cache_key("student_applications")
    cached = cache.get(cache_key)
    if cached is not None:
        return jsonify(cached)

    student = Student.query.filter_by(user_id=session["id"]).first()

    if not student:
        return jsonify({"message": "Student not found"}), 404

    applications = Application.query.filter_by(student_id=student.id).all()

    result = []

    for app in applications:

        result.append({

            "id": app.id,
            "drive_id": app.drive.id,
            "drive": app.drive.title,
            "company": app.company.Companyname,
          
            "status": app.status,
            "result": app.result

        })

    payload = {
        "applications": result
    }
    cache.set(cache_key, payload, timeout=300)
    return jsonify(payload)

@app.route("/student/history")
def student_history():

    if session.get("role") != "student":
        return jsonify({"message": "Unauthorized"}), 401

    cache_key = get_cache_key("student_history")
    cached = cache.get(cache_key)
    if cached is not None:
        return jsonify(cached)

    student = Student.query.filter_by(user_id=session["id"]).first()
    if student is None:
        return jsonify({"message": "Student not found"}), 404

    applications = Application.query.filter_by(student_id=student.id).all()

    history = []

    for app in applications:

        drive = Drive.query.get(app.drive_id)
        if not drive:
            continue

        company = Company.query.get(drive.company_id) if drive.company_id else None

        # find interview related to this application
        interview = Interview.query.filter_by(application_id=app.id).first()

        history.append({
            "id": app.id,
            "drive": drive.title if drive else "",
            "company": company.Companyname if company else "",
            "interview_mode": interview.mode if interview else "",
            "interview_date": interview.interview_date.strftime("%Y-%m-%d") if interview and interview.interview_date else "",
            "result": app.result
        })
    payload = {
        "history": history
    }
    try:
        cache.set(cache_key, payload, timeout=300)
    except Exception:
        app.logger.debug(f"cache.set error for {cache_key}")
    return jsonify(payload)

@app.route(
    "/student/export_applications",
    methods=["POST"]
)
def export_applications():

    if session.get("role")!="student":
        return jsonify({"message":"Unauthorized"}),401

    student = Student.query.filter_by(
        user_id=session["id"]
    ).first()

    job = ExportJob(
        student_id=student.id
    )

    db.session.add(job)

    db.session.commit()

    
    from tasks import export_student_applications
    export_student_applications.delay(job.id)

    return jsonify({

        "job_id":job.id,

        "message":"Export Started"

    })

@app.route("/student/export/status/<int:id>")
def export_status(id):

    student = Student.query.filter_by(
        user_id=session["id"]
    ).first()

    job = ExportJob.query.get(id)

    if not job:
        return jsonify({"message":"Not Found"}),404

    if job.student_id != student.id:
        return jsonify({"message":"Unauthorized"}),401

    return jsonify({

        "status":job.status,

        "file":job.file_name

    })

@app.route("/student/export/download/<int:id>")
def download_export(id):

    student = Student.query.filter_by(
        user_id=session["id"]
    ).first()

    job = ExportJob.query.get(id)

    if job.student_id != student.id:
        return jsonify({"message":"Unauthorized"}),401

    return send_file(
        job.file_name,
        as_attachment=True
    )
