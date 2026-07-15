from faker import Faker
from faker_food import FoodProvider
import random
import uuid
from datetime import datetime, timedelta, timezone

from flask_security.utils import hash_password

from app import app
from extension import db
from models import User, Role, Student, Company, PlacementDrive, Application


fake = Faker()
fake.add_provider(FoodProvider)


def seed_data():
    with app.app_context():

        print("🔄 Seeding database...")

        roles = {}

        for role_name in ["admin", "manager", "student"]:
            existing_role = Role.query.filter_by(name=role_name).first()

            if existing_role:
                roles[role_name] = existing_role
            else:
                role = Role(name=role_name)
                db.session.add(role)
                roles[role_name] = role

        db.session.commit()

        managers = []

        for _ in range(5):
            user = User(
                email=fake.unique.email(),
                password=hash_password("password"),
                active=True,
                fs_uniquifier=str(uuid.uuid4()),
                created_at=fake.date_time_between(
                    start_date="-60d", end_date="now", tzinfo=timezone.utc
                )
            )

            user.roles.append(roles["manager"])
            db.session.add(user)
            db.session.flush()

            company = Company(
                user_id=user.id,
                company_name=fake.company(),
                website=fake.url(),
                hr_name=fake.name(),
                hr_email=fake.email(),
                hr_phone=f"{random.randint(6000000000, 9999999999)}",
                approval_status=random.choice(["Pending", "Approved"]),
                created_at=user.created_at
            )

            db.session.add(company)
            managers.append(company)

        students = []

        for _ in range(20):
            user = User(
                email=fake.unique.email(),
                password=hash_password("password"),
                active=True,
                fs_uniquifier=str(uuid.uuid4()),
                created_at=fake.date_time_between(
                    start_date="-90d", end_date="now", tzinfo=timezone.utc
                )
            )

            user.roles.append(roles["student"])
            db.session.add(user)
            db.session.flush()

            student = Student(
                user_id=user.id,
                name=fake.name(),
                roll_no=f"2026{fake.unique.random_int(min=1000, max=9999)}",
                branch=random.choice(["CSE", "IT", "ECE", "ME"]),
                cgpa=round(random.uniform(6.0, 9.8), 2),
                year=random.randint(2, 4),
                phone=f"{random.randint(6000000000, 9999999999)}",
                is_placed=False,
                created_at=user.created_at
            )

            db.session.add(student)
            students.append(student)

        db.session.commit()

        drives = []

        base_date = datetime.now(timezone.utc) - timedelta(days=60)

        for i in range(15):
            company = random.choice(managers)
            created_date = base_date + timedelta(days=i * 3)

            drive = PlacementDrive(
                company_id=company.id,
                job_title=fake.job(),
                job_description=fake.text(),
                salary=f"{random.randint(4,20)} LPA",
                eligibility_branch=random.choice(["CSE", "IT", "ECE"]),
                min_cgpa=round(random.uniform(6.0, 8.5), 2),
                eligible_year=random.randint(3, 4),
                application_deadline=(created_date + timedelta(days=10)).date(),
                status=random.choice(["Pending", "Approved", "Closed"]),
                created_at=created_date
            )

            db.session.add(drive)
            drives.append(drive)

        db.session.commit()

        for _ in range(50):
            student = random.choice(students)
            drive = random.choice(drives)

            # prevent duplicate applications
            exists = Application.query.filter_by(
                student_id=student.id,
                drive_id=drive.id
            ).first()

            if exists:
                continue

            app_date = drive.created_at + timedelta(days=random.randint(1, 7))

            application = Application(
                student_id=student.id,
                drive_id=drive.id,
                application_date=app_date,
                status=random.choice(
                    ["Applied", "Shortlisted", "Selected", "Rejected"]
                )
            )

            db.session.add(application)

        db.session.commit()

        print("Seeding complete!")

        print("Users:", User.query.count())
        print("Students:", Student.query.count())
        print("Companies:", Company.query.count())
        print("Drives:", PlacementDrive.query.count())
        print("Applications:", Application.query.count())


if __name__ == "__main__":
    seed_data()