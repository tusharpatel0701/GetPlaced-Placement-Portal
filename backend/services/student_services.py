import os
from models import Student, PlacementDrive, Application, db
from datetime import datetime
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "uploads/resumes"
ALLOWED_EXTENSIONS = {"pdf"}


# GET STUDENT PROFILE
def get_student_profile(student_id):
    student = Student.query.get(student_id)
    if not student:
        return {"message": "Student not found"}, 404

    data = {
        "id": student.id,
        "name": student.name,
        "roll_no": student.roll_no,
        "branch": student.branch,
        "cgpa": student.cgpa,
        "year": student.year,
        "phone": student.phone,
        "is_placed": student.is_placed,
        "resume_path": student.resume_path,
    }

    return data, 200


# UPDATE STUDENT PROFILE
def update_student_profile(student_id, data):
    student = Student.query.get(student_id)
    if not student:
        return {"message": "Student not found"}, 404

    student.name = data.get("name", student.name)
    student.branch = data.get("branch", student.branch)
    student.phone = data.get("phone", student.phone)
    student.cgpa = float(data.get("cgpa", student.cgpa))
    student.year = int(data.get("year", student.year))

    db.session.commit()

    return {"message": "Profile updated successfully"}, 200


# UPLOAD RESUME
def upload_resume(student_id, files):
    student = Student.query.get(student_id)
    if not student:
        return {"message": "Student not found"}, 404

    if "resume" not in files:
        return {"message": "No file provided"}, 400

    file = files["resume"]

    if file.filename == "":
        return {"message": "No file selected"}, 400

    if not file.filename.lower().endswith(".pdf"):
        return {"message": "Only PDF files are allowed"}, 400

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    filename = secure_filename(f"student_{student_id}_{file.filename}")
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    file.save(filepath)

    student.resume_path = filepath
    db.session.commit()

    return {"message": "Resume uploaded successfully", "path": filepath}, 200


# GET ALL APPROVED DRIVES
def get_all_approved_drives():
    drives = PlacementDrive.query.filter_by(status="Approved").all()

    data = [{
        "id": d.id,
        "job_title": d.job_title,
        "job_description": d.job_description,
        "company_name": d.company.company_name,
        "salary": d.salary,
        "eligibility_branch": d.eligibility_branch,
        "min_cgpa": d.min_cgpa,
        "eligible_year": d.eligible_year,
        "application_deadline": d.application_deadline.strftime("%Y-%m-%d") if d.application_deadline else None,
    } for d in drives]

    return data, 200


# APPLY FOR DRIVE
def apply_for_drive(drive_id, data):
    student_id = data.get("student_id")

    if not student_id:
        return {"message": "student_id is required"}, 400

    drive = PlacementDrive.query.get(drive_id)

    if not drive:
        return {"message": "Drive not found"}, 404

    if drive.status != "Approved":
        return {"message": "Drive is not open for applications"}, 400

    existing = Application.query.filter_by(
        student_id=student_id,
        drive_id=drive_id
    ).first()

    if existing:
        return {"message": "Already applied for this drive"}, 400

    application = Application(
        student_id=student_id,
        drive_id=drive_id,
        status="Applied"
    )

    db.session.add(application)
    db.session.commit()

    return {"message": "Application submitted successfully"}, 201


# GET STUDENT APPLICATIONS
def get_student_applications(student_id):
    student = Student.query.get(student_id)

    if not student:
        return {"message": "Student not found"}, 404

    apps = Application.query.filter_by(student_id=student_id).all()

    data = [{
        "id": app.id,
        "drive_id": app.drive_id,
        "job_title": app.drive.job_title,
        "company_name": app.drive.company.company_name,
        "salary": app.drive.salary,
        "applied_on": app.application_date.strftime("%Y-%m-%d") if app.application_date else None,
        "status": app.status,
    } for app in apps]

    return data, 200


# TRIGGER CSV EXPORT
def trigger_csv_export(student_id):
    from app import celery

    student = Student.query.get(student_id)

    if not student:
        return {"message": "Student not found"}, 404

    task = celery.send_task(
        "tasks.export_csv.export_student_applications",
        args=[student_id]
    )

    return {
        "message": "Export started! You'll receive an email shortly.",
        "task_id": task.id
    }, 202