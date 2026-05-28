from app import app
from extension import db
from flask_security import SQLAlchemyUserDatastore, hash_password
from models import User, Role, Student, Company
import uuid

with app.app_context():

    datastore: SQLAlchemyUserDatastore = app.datastore

    admin_role = datastore.find_or_create_role(
        name="admin", description="admin user"
    )
    manager_role = datastore.find_or_create_role(
        name="manager", description="manager user"
    )
    student_role = datastore.find_or_create_role(
        name="student", description="student user"
    )

    db.session.commit() # ensure roles exist

    # CREATE ADMIN 
    admin = datastore.find_user(email="tusharpat0701@gmail.com")

    if not admin:
        admin = datastore.create_user(
            email="tusharpat0701@gmail.com",
            password=hash_password("admin123"),
            fs_uniquifier=str(uuid.uuid4())
        )
        datastore.add_role_to_user(admin, admin_role)


    # CREATE MANAGER 
    manager = datastore.find_user(email="manager@test.com")

    if not manager:
        manager = datastore.create_user(
            email="manager@test.com",
            password=hash_password("manager123"),
            fs_uniquifier=str(uuid.uuid4())
        )
        datastore.add_role_to_user(manager, manager_role)

    db.session.flush()  # ensure IDs available

    # create company profile if not exists
    if not manager.company_profile:
        company = Company(
            user_id=manager.id,
            company_name="Tech Corp",
            website="https://techcorp.com",
            hr_name="Rahul Sharma",
            hr_email="hr@techcorp.com",
            hr_phone="9876543210",
            approval_status="Approved"
        )
        db.session.add(company)

    # CREATE STUDENT (SAFE)

    student = datastore.find_user(email="student@test.com")

    if not student:
        student = datastore.create_user(
            email="student@test.com",
            password=hash_password("student123"),
            fs_uniquifier=str(uuid.uuid4())
        )
        datastore.add_role_to_user(student, student_role)

    db.session.flush()

    # create student profile if not exists
    if not student.student_profile:
        student_profile = Student(
            user_id=student.id,
            name="Tushar",
            roll_no="CS2026001",
            branch="CSE",
            cgpa=8.5,
            year=2026,
            phone="9123456780"
        )
        db.session.add(student_profile)


    # FINAL COMMIT
    
    try:
        db.session.commit()
        print("✅ Admin, Manager, Student initialized successfully (no duplicates)")
    except Exception as e:
        db.session.rollback()
        print("Error:", e)