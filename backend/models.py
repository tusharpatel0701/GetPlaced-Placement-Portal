from extension import db
from datetime import datetime, timezone
from flask_security import UserMixin, RoleMixin
import uuid


# ASSOCIATION TABLE (M2M)

roles_users = db.Table(
    "roles_users",
    db.Column("user_id", db.Integer(), db.ForeignKey("users.id")),
    db.Column("role_id", db.Integer(), db.ForeignKey("roles.id"))
)


# ROLE TABLE
class Role(db.Model, RoleMixin):
    __tablename__ = "roles"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255))


# USER TABLE

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)

    # Flask-Security required fields
    active = db.Column(db.Boolean(), default=True)
    fs_uniquifier = db.Column(
        db.String(255),
        unique=True,
        nullable=False,
        default=lambda: str(uuid.uuid4())
    )

    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    roles = db.relationship(
        "Role",
        secondary=roles_users,
        backref=db.backref("users", lazy="dynamic")
    )

    student_profile = db.relationship(
        "Student",
        backref="user",
        uselist=False,
        cascade="all, delete"
    )

    company_profile = db.relationship(
        "Company",
        backref="user",
        uselist=False,
        cascade="all, delete"
    )


# STUDENT TABLE

class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        unique=True
    )

    name = db.Column(db.String(100), nullable=False, index=True)

    roll_no = db.Column(
        db.String(50),
        unique=True,
        nullable=False,
        index=True
    )

    branch = db.Column(db.String(100), nullable=False)

    cgpa = db.Column(db.Float, nullable=False)

    year = db.Column(db.Integer, nullable=False)

    phone = db.Column(db.String(15), nullable=False)

    resume_path = db.Column(db.String(255))

    is_placed = db.Column(db.Boolean, default=False)

    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # relationships
    applications = db.relationship(
        "Application",
        backref="student",
        lazy=True,
        cascade="all, delete"
    )



# COMPANY TABLE
class Company(db.Model):
    __tablename__ = "companies"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        unique=True
    )

    company_name = db.Column(
        db.String(150),
        nullable=False,
        index=True
    )

    website = db.Column(db.String(255))

    hr_name = db.Column(db.String(100))

    hr_email = db.Column(db.String(120))

    hr_phone = db.Column(db.String(15))

    approval_status = db.Column(
        db.String(20),
        default="Pending"
    )  # Pending / Approved / Rejected / Blacklisted

    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # relationships
    drives = db.relationship(
        "PlacementDrive",
        backref="company",
        lazy=True,
        cascade="all, delete"
    )


# PLACEMENT DRIVE

class PlacementDrive(db.Model):
    __tablename__ = "placement_drives"

    id = db.Column(db.Integer, primary_key=True)

    company_id = db.Column(
        db.Integer,
        db.ForeignKey("companies.id"),
        nullable=False
    )

    job_title = db.Column(db.String(150), nullable=False)

    job_description = db.Column(db.Text, nullable=False)

    salary = db.Column(db.String(50))

    eligibility_branch = db.Column(db.String(100), nullable=False)

    min_cgpa = db.Column(db.Float, nullable=False)

    eligible_year = db.Column(db.Integer, nullable=False)

    application_deadline = db.Column(db.Date, nullable=False)

    status = db.Column(
        db.String(20),
        default="Pending"
    )  # Pending / Approved / Rejected / Closed

    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # relationships
    applications = db.relationship(
        "Application",
        backref="drive",
        lazy=True,
        cascade="all, delete"
    )



# APPLICATION TABLE
class Application(db.Model):
    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("students.id"),
        nullable=False
    )

    drive_id = db.Column(
        db.Integer,
        db.ForeignKey("placement_drives.id"),
        nullable=False
    )

    application_date = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    status = db.Column(
        db.String(20),
        default="Applied"
    )  # Applied / Shortlisted / Selected / Rejected

    __table_args__ = (
        db.UniqueConstraint(
            "student_id",
            "drive_id",
            name="unique_student_drive"
        ),
    )