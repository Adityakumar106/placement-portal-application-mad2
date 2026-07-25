from flask import request, session, jsonify
from App import app
from App import cache
from database.database import db
from models.models import User, Student, Company, Drive, Application, Interview


def get_cache_key(prefix: str):
    user_id = session.get("id")
    role = session.get("role")
    return f"{prefix}:{role}:{user_id}"


def admin_required():
    if session.get("role") != "admin":
        return False
    return True


@app.route("/admin/dashboard")
def admin_dashboard():
    if not admin_required():
        return jsonify({"message": "Unauthorized"}), 401

    cache_key = get_cache_key("admin_dashboard")
    cached = cache.get(cache_key)
    if cached is not None:
        return jsonify(cached)

    students = Student.query.count()
    companies = Company.query.count()
    drives = Drive.query.count()
    applications = Application.query.count()
    payload = {
        "students": students,
        "companies": companies,
        "drives": drives,
        "applications": applications
    }
    cache.set(cache_key, payload, timeout=300)
    return jsonify(payload)


@app.route("/admin/students")
def admin_students():
    if not admin_required():
        return jsonify({"message": "Unauthorized"}), 401

    cache_key = get_cache_key("admin_students")
    cached = cache.get(cache_key)
    if cached is not None:
        return jsonify(cached)

    students = Student.query.all()

    result = []
    for student in students:
        result.append({
            "id": student.id,
            "username": student.username,
            "blacklisted": student.user.blacklisted if student.user else False
        })
    payload = {"students": result}
    cache.set(cache_key, payload, timeout=300)
    return jsonify(payload)


@app.route("/admin/student/<int:id>/blacklist", methods=["POST"])
def blacklist_student(id):
    if not admin_required():
        return jsonify({"message": "Unauthorized"}), 401

    student = Student.query.get_or_404(id)
    user = student.user

    if user is None:
        return jsonify({"message": "User not found"}), 404

    user.blacklisted = True
    db.session.commit()
    cache.clear()

    return jsonify({"message": "Student blacklisted successfully"})


@app.route("/admin/companies")
def admin_companies():
    if not admin_required():
        return jsonify({"message": "Unauthorized"}), 401

    cache_key = get_cache_key("admin_companies")
    cached = cache.get(cache_key)
    if cached is not None:
        return jsonify(cached)

    companies = Company.query.all()

    result = []
    for company in companies:
        result.append({
            "id": company.id,
            "companyname": company.Companyname,
            "approved": company.approved,
            "rejected": company.rejected,
            "blacklisted": company.user.blacklisted if company.user else False
        })
    payload = {"companies": result}
    cache.set(cache_key, payload, timeout=300)
    return jsonify(payload)


@app.route("/admin/company/<int:id>/approve", methods=["POST"])
def approve_company(id):
    if not admin_required():
        return jsonify({"message": "Unauthorized"}), 401

    company = Company.query.get_or_404(id)
    company.approved = True
    company.rejected = False
    db.session.commit()
    cache.clear()

    return jsonify({"message": "Company approved successfully"})


@app.route("/admin/company/<int:id>/reject", methods=["POST"])
def reject_company(id):
    if not admin_required():
        return jsonify({"message": "Unauthorized"}), 401

    company = Company.query.get_or_404(id)
    company.approved = False
    company.rejected = True
    db.session.commit()
    cache.clear()

    return jsonify({"message": "Company rejected successfully"})


@app.route("/admin/company/<int:id>/blacklist", methods=["POST"])
def blacklist_company(id):
    if not admin_required():
        return jsonify({"message": "Unauthorized"}), 401

    company = Company.query.get_or_404(id)
    user = company.user

    if user is None:
        return jsonify({"message": "User not found"}), 404

    user.blacklisted = True
    db.session.commit()
    cache.clear()

    return jsonify({"message": "Company blacklisted successfully"})


@app.route("/admin/drives")
def admin_drives():
    if not admin_required():
        return jsonify({"message": "Unauthorized"}), 401

    cache_key = get_cache_key("admin_drives")
    cached = cache.get(cache_key)
    if cached is not None:
        return jsonify(cached)

    drives = Drive.query.all()

    result = []
    for drive in drives:
        company = Company.query.get(drive.company_id)
        result.append({
            "id": drive.id,
            "title": drive.title,
            "company": company.Companyname if company else "",
            "status": drive.status
        })
    payload = {"drives": result}
    cache.set(cache_key, payload, timeout=300)
    return jsonify(payload)


@app.route("/admin/drive/<int:id>/complete", methods=["POST"])
def complete_admin_drive(id):
    if not admin_required():
        return jsonify({"message": "Unauthorized"}), 401

    drive = Drive.query.get_or_404(id)
    drive.status = "closed"
    db.session.commit()
    cache.clear()

    return jsonify({"message": "Drive marked as completed"})


@app.route("/admin/drive/<int:id>")
def admin_drive_details(id):
    if not admin_required():
        return jsonify({"message": "Unauthorized"}), 401

    cache_key = get_cache_key(f"admin_drive_{id}")
    cached = cache.get(cache_key)
    if cached is not None:
        return jsonify(cached)

    drive = Drive.query.get_or_404(id)
    company = Company.query.get(drive.company_id)
    payload = {
        "id": drive.id,
        "title": drive.title,
        "company": company.Companyname if company else "",
        "job_title": drive.job_title,
        "description": drive.description,
        "eligibility": drive.eligibility,
        "salary": drive.salary,
        "deadline": drive.deadline.strftime("%Y-%m-%d") if drive.deadline else "",
        "status": drive.status
    }
    cache.set(cache_key, payload, timeout=300)
    return jsonify(payload)


@app.route("/admin/applications")
def admin_applications():
    if not admin_required():
        return jsonify({"message": "Unauthorized"}), 401

    cache_key = get_cache_key("admin_applications")
    cached = cache.get(cache_key)
    if cached is not None:
        return jsonify(cached)

    applications = Application.query.all()

    result = []
    for application in applications:
        student = Student.query.get(application.student_id)
        company = Company.query.get(application.company_id)
        drive = Drive.query.get(application.drive_id)

        result.append({
            "id": application.id,
            "student": student.username if student else "",
            "company": company.Companyname if company else "",
            "drive": drive.title if drive else "",
            "status": application.status,
            "result": application.result
        })
    payload = {"applications": result}
    cache.set(cache_key, payload, timeout=300)
    return jsonify(payload)


@app.route("/admin/application/<int:id>")
def admin_application_details(id):
    if not admin_required():
        return jsonify({"message": "Unauthorized"}), 401

    cache_key = get_cache_key(f"admin_application_{id}")
    cached = cache.get(cache_key)
    if cached is not None:
        return jsonify(cached)

    application = Application.query.get_or_404(id)
    student = Student.query.get(application.student_id)
    company = Company.query.get(application.company_id)
    drive = Drive.query.get(application.drive_id)
    user = student.user if student and student.user else None

    payload = {
        "id": application.id,
        "status": application.status,
        "result": application.result,
        "applied_on": application.applied_on.strftime("%Y-%m-%d") if application.applied_on else "",
        "student": {
            "id": student.id if student else None,
            "username": student.username if student else "",
            "email": user.email if user else "",
            "degree": student.degree if student else "",
            "course": student.course if student else "",
            "branch": student.branch if student else "",
            "cgpa": student.cgpa if student else "",
            "phone": student.phone if student else "",
            "linkedin": student.linkdin if student else "",
            "about": student.about if student else "",
            "resume": student.resume if student else ""
        },
        "company": company.Companyname if company else "",
        "drive": drive.title if drive else ""
    }
    cache.set(cache_key, payload, timeout=300)
    return jsonify(payload)


