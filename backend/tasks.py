from celeryworker import celery
from datetime import date, timedelta, datetime
from models.models import User, Student, Drive, Application, ExportJob
from database.database import db
from mail import send_mail
import csv
import os

@celery.task
def daily_reminder():

    tomorrow = date.today() + timedelta(days=1)

    drives = Drive.query.filter(
        Drive.deadline == tomorrow,
        Drive.status == "open"
    ).all()

    for drive in drives:

        students = Student.query.all()

        for student in students:

            user = User.query.get(student.user_id)

            if not user:
                continue

            subject = f"Reminder: {drive.title}"

            body = f"""
Hello {student.username},

The placement drive "{drive.title}" conducted by
{drive.company.Companyname}

is closing tomorrow.

Job Role : {drive.job_title}

Deadline : {drive.deadline}

Please apply before the deadline.

Placement Portal
"""

            send_mail(user.email, subject, body)

    return "Daily Reminder Completed"

@celery.task
def monthly_report():

    total_drives = Drive.query.count()

    total_applications = Application.query.count()

    total_selected = Application.query.filter_by(
        result="Selected"
    ).count()

    html = f"""
    <html>

    <body>

    <h2>Monthly Placement Report</h2>

    <table border="1" cellpadding="10">

    <tr>

    <th>Metric</th>
    <th>Count</th>

    </tr>

    <tr>

    <td>Placement Drives</td>
    <td>{total_drives}</td>

    </tr>

    <tr>

    <td>Applications</td>
    <td>{total_applications}</td>

    </tr>

    <tr>

    <td>Students Selected</td>
    <td>{total_selected}</td>

    </tr>

    </table>

    <br>

    Generated on

    {datetime.now()}

    </body>

    </html>
    """

    admin = User.query.filter_by(role="admin").first()

    send_mail(
        admin.email,
        "Monthly Placement Report",
        html,
        is_html=True
    )

    return "Monthly Report Sent"

@celery.task
def export_student_applications(job_id):

    job = ExportJob.query.get(job_id)

    if not job:
        return

    job.status = "Processing"
    db.session.commit()

    applications = Application.query.filter_by(
        student_id=job.student_id
    ).all()

    os.makedirs("exports", exist_ok=True)

    filename = f"exports/student_{job.student_id}.csv"

    with open(
        filename,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([

            "Student ID",

            "Company Name",

            "Drive Title",

            "Application Status",

            "Applied Date"

        ])

        for app in applications:

            writer.writerow([

                app.student_id,

                app.company.Companyname,

                app.drive.title,

                app.status,

                app.applied_on.strftime("%d-%m-%Y")

            ])

    job.file_name = filename

    job.status = "Completed"

    db.session.commit()

    student = Student.query.get(job.student_id)

    user = User.query.get(student.user_id)

    send_mail(

        user.email,

        "CSV Export Completed",

        "Your application history CSV is ready."

    )

    return filename