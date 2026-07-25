from flask import request, session,jsonify
from App import app
from App import cache
from database.database import db
from models.models import Company, User, Drive, Student, Application,Interview
from datetime import datetime


def get_cache_key(prefix: str):
    user_id = session.get("id")
    role = session.get("role")
    return f"{prefix}:{role}:{user_id}"

@app.route("/company/dashboard")
def company_dashboard():
    
    if session.get("role") != "company":
        return {"message":"Unauthorized"},401
    company=Company.query.filter_by(user_id=session["id"],approved=True).first()
    if not company:
        return {"message": "Company not found or not approved"}, 404
    return {"message": "Welcome to the Company Dashboard!" }

@app.route("/company/profile", methods=["GET"])
def company_profile():

    if session.get("role") != "company":
        return jsonify({"message": "Unauthorized"}), 401

    cache_key = get_cache_key("company_profile")
    cached = cache.get(cache_key)
    if cached is not None:
        return jsonify(cached)

    company = Company.query.filter_by(user_id=session["id"]).first()

    if not company:
        return jsonify({"message": "Company not found"}), 404

    payload = {
        "Companyname": company.Companyname,
        "hrcontact": company.hrcontact,
        "website": company.website,
        "approved": company.approved
    }
    cache.set(cache_key, payload, timeout=300)
    return jsonify(payload)


@app.route("/company/profile", methods=["PUT"])
def update_company_profile():

    if session.get("role") != "company":
        return jsonify({"message": "Unauthorized"}), 401

    company = Company.query.filter_by(user_id=session["id"]).first()

    if not company:
        return jsonify({"message": "Company not found"}), 404

    data = request.get_json()

    company.Companyname = data.get("Companyname")
    company.hrcontact = data.get("hrcontact")
    company.website = data.get("website")

    db.session.commit()

    
    try:
        cache_key = get_cache_key("company_profile")
        cache.delete(cache_key)
    except Exception:
        pass

    return jsonify({
        "message": "Profile updated successfully"
    })


@app.route("/company/create-drive", methods=["POST"])
def create_drive():

    if session.get("role") != "company":
        return jsonify({"message": "Unauthorized"}), 401

    company = Company.query.filter_by(user_id=session["id"]).first()

    if not company:
        return jsonify({"message": "Company not found"}), 404

    data = request.get_json()

    drive = Drive(
        company_id=company.id,
        title=data.get("title"),
        job_title=data.get("job_title"),
        description=data.get("description"),
        eligibility=data.get("eligibility"),
        salary=data.get("salary"),
        deadline=None
    )

    # parse deadline if provided
    if data.get("deadline"):
        try:
            drive.deadline = datetime.strptime(data.get("deadline"), "%Y-%m-%d").date()
        except Exception:
            return jsonify({"message": "Invalid deadline format, expected YYYY-MM-DD"}), 400

    db.session.add(drive)
    db.session.commit()
    cache.clear()

    return jsonify({
        "message": "Placement drive created successfully",
        "drive": {
            "id": drive.id,
            "title": drive.title,
            "status": drive.status
        }
    }), 201

@app.route("/company/drives")
def company_drives():

    if session.get("role") != "company":
        return jsonify({"message":"Unauthorized"}),401

    company = Company.query.filter_by(user_id=session.get("id")).first()

    if not company:
        return jsonify({"message": "Company not found"}), 404

    drives = Drive.query.filter_by(company_id=company.id).all()
    app.logger.debug(f"company_drives: company_id={company.id} drives={len(drives)}")
    payload = {
        "drives":[
            {
                "id":d.id,
                "title":d.title,
                "status":d.status
            }
            for d in drives
        ]
    }
    return jsonify(payload)


@app.route("/company/drive/<int:id>/complete", methods=["POST"])
def complete_drive(id):

    if session.get("role") != "company":
        return jsonify({"message":"Unauthorized"}),401

    drive = Drive.query.get_or_404(id)

    drive.status = "closed"

    db.session.commit()
    cache.clear()

    return jsonify({"message":"Drive closed"})

@app.route("/company/drive/<int:id>/restart", methods=["POST"])
def restart_drive(id):

    if session.get("role") != "company":
        return jsonify({"message":"Unauthorized"}),401

    drive = Drive.query.get_or_404(id)

    drive.status = "open"

    db.session.commit()
    cache.clear()

    return jsonify({"message":"Drive restarted"})

@app.route("/company/drive/<int:id>")
def drive_details(id):

    if session.get("role") != "company":
        return jsonify({"message":"Unauthorized"}),401

    cache_key = get_cache_key(f"company_drive_{id}")
    cached = cache.get(cache_key)
    if cached is not None:
        return jsonify(cached)

    company = Company.query.filter_by(
        user_id=session.get("id")
    ).first()

    if not company:
        return jsonify({"message": "Company not found"}), 404

    drive = Drive.query.filter_by(
        id=id,
        company_id=company.id
    ).first()

    if drive is None:
        return jsonify({"message":"Drive not found"}),404

    applications = Application.query.filter_by(
        drive_id=id
    ).all()

    students=[]

    for application in applications:

        student = Student.query.get(application.student_id)

        students.append({

            "id":student.id,
            "username":student.username

        })
    deadline_value = drive.deadline.strftime("%Y-%m-%d") if drive.deadline else ""

    payload = {

        "drive":{

            "id":drive.id,
            "title":drive.title,
            "job_title":drive.job_title,
            "description":drive.description,
            "eligibility":drive.eligibility,
            "salary":drive.salary,
            "deadline": deadline_value,
            "status":drive.status

        },

        "students":students

    }
    cache.set(cache_key, payload, timeout=300)
    return jsonify(payload)

@app.route("/company/application/<int:drive_id>/<int:student_id>")
def company_application(drive_id, student_id):

    if session.get("role") != "company":
        return jsonify({"message": "Unauthorized"}), 401

    cache_key = get_cache_key(f"company_application_{drive_id}_{student_id}")
    cached = cache.get(cache_key)
    if cached is not None:
        return jsonify(cached)

    application = Application.query.filter_by(
        drive_id=drive_id,
        student_id=student_id
    ).first()

    if application is None:
        return jsonify({"message": "Application not found"}), 404

    student = application.student
    user = student.user
    interview = application.interview
    payload = {

        "username": student.username,
        "email": user.email,
        "degree": student.degree,
        "course": student.course,
        "branch": student.branch,
        "cgpa": student.cgpa,
        "phone": student.phone,
        "linkedin": student.linkdin,
        "about": student.about,
        "resume": student.resume,

        "company": application.company.Companyname,
        "drive": application.drive.title,

        "result": application.result,

        "mode": interview.mode if interview else "",

        "interview_date":
            interview.interview_date.strftime("%Y-%m-%d")
            if interview and interview.interview_date else ""

    }
    cache.set(cache_key, payload, timeout=300)
    return jsonify(payload)


@app.route("/company/application/<int:drive_id>/<int:student_id>", methods=["PUT"])
def update_company_application(drive_id, student_id):

    if session.get("role") != "company":
        return jsonify({"message": "Unauthorized"}), 401

    application = Application.query.filter_by(
        drive_id=drive_id,
        student_id=student_id
    ).first()

    if application is None:
        return jsonify({"message": "Application not found"}), 404

    data = request.get_json()

    # Update application result
    application.result = data.get("result")

    # Create interview if it doesn't exist
    interview = Interview.query.filter_by(
        application_id=application.id
    ).first()

    if interview is None:

        interview = Interview(
            application_id=application.id
        )

        db.session.add(interview)

    interview.mode = data.get("mode")

    if data.get("interview_date"):

        interview.interview_date = datetime.strptime(
            data.get("interview_date"),
            "%Y-%m-%d"
        )

    else:

        interview.interview_date = None

    db.session.commit()
    cache.clear()

    return jsonify({
        "message": "Application updated successfully."
    })
