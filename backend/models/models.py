from database.database import db
from flask_login import UserMixin
from datetime import datetime

# Universal User (Auth Table)
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(20)) 
    blacklisted = db.Column(db.Boolean, default=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_active = db.Column(db.Boolean, default=True)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    username = db.Column(db.String(150))
    resume = db.Column(db.String(200))
    degree = db.Column(db.String(200))
    course = db.Column(db.String(200))
    branch = db.Column(db.String(200))
    cgpa = db.Column(db.String(50))
    phone = db.Column(db.String(50))
    linkdin = db.Column(db.String(200))
    about = db.Column(db.String(500))
    user = db.relationship(
        "User",
        backref="student",
        uselist=False
    )

    @property
    def linkedin(self):
        return self.linkdin

    @linkedin.setter
    def linkedin(self, value):
        self.linkdin = value
    
    

# Company Profile
class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    Companyname = db.Column(db.String(150))
    hrcontact = db.Column(db.String(100))
    website = db.Column(db.String(200))
    approved = db.Column(db.Boolean, default=False)
    rejected = db.Column(db.Boolean, default=False)
    user = db.relationship(
        "User",
        backref="company",
        uselist=False
    )

# Placement Drive
class Drive(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    title=db.Column(db.String(20))
    job_title = db.Column(db.String(150))
    description = db.Column(db.Text)
    eligibility = db.Column(db.String(200))
    deadline = db.Column(db.Date)
    salary=db.Column(db.String(20))
    status = db.Column(db.String(50), default="open")
    company= db.relationship('Company', backref='drive')

# Application
class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    drive_id = db.Column(db.Integer, db.ForeignKey('drive.id'))
    applied_on = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default="Applied")
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    drive = db.relationship('Drive', backref='applications')
    student = db.relationship('Student', backref='applications')
    result=db.Column(db.String(50), default="Waiting")
    student = db.relationship(
        "Student",
        backref="applications"
    )

    drive = db.relationship(
        "Drive",
        backref="applications"
    )

    company = db.relationship(
        "Company",
        backref="applications"
    )

    __table_args__ = (
        db.UniqueConstraint(
            "student_id",
            "drive_id",
            name="unique_application"
        ),
    )


class Interview(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    application_id = db.Column(
        db.Integer,
        db.ForeignKey("application.id")
    )

    interview_date = db.Column(db.DateTime)

    mode = db.Column(db.String(50))


    application = db.relationship(
        "Application",
        backref="interview",
        uselist=False
    )

class ExportJob(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("student.id")
    )

    status = db.Column(
        db.String(20),
        default="Pending"
    )

    file_name = db.Column(
        db.String(300)
    )

    created_on = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

