from models import Company, PlacementDrive, Application, db
from datetime import datetime, date
from extension import cache                         # ✅ ADD THIS


# GET COMPANY PROFILE
def get_company_profile(company_id):
    key = f"company_profile_{company_id}"
    data = cache.get(key)
    if data is None:
        company = Company.query.get(company_id)
        if not company:
            return {"message": "Company not found"}, 404
        data = {
            "id": company.id,
            "company_name": company.company_name,
            "website": company.website,
            "hr_name": company.hr_name,
            "hr_email": company.hr_email,
            "hr_phone": company.hr_phone,
            "approval_status": company.approval_status,
        }
        cache.set(key, data, timeout=300)                      # 5 mins
    return data, 200


# GET COMPANY DRIVES
def get_company_drives(company_id):
    key = f"company_drives_{company_id}"
    data = cache.get(key)
    if data is None:
        company = Company.query.get(company_id)
        if not company:
            return {"message": "Company not found"}, 404
        drives = PlacementDrive.query.filter_by(company_id=company_id).all()
        data = [{
            "id": d.id,
            "job_title": d.job_title,
            "job_description": d.job_description,
            "eligibility_branch": d.eligibility_branch,
            "min_cgpa": d.min_cgpa,
            "eligible_year": d.eligible_year,
            "salary": d.salary,
            "status": d.status,
            "application_deadline": d.application_deadline.strftime("%Y-%m-%d") if d.application_deadline else None,
            "applicant_count": len(d.applications),
        } for d in drives]
        cache.set(key, data, timeout=180)                      # 3 mins
    return data, 200


# CREATE DRIVE
def create_drive(data):
    try:
        deadline_str = data.get("application_deadline")
        if not deadline_str:
            return {"message": "application_deadline is required"}, 400
        try:
            deadline = datetime.strptime(deadline_str, "%Y-%m-%d").date()
        except ValueError:
            return {"message": "Invalid date format. Use YYYY-MM-DD"}, 400
        drive = PlacementDrive(
            company_id=data.get("company_id"),
            job_title=data.get("job_title"),
            job_description=data.get("job_description"),
            eligibility_branch=data.get("eligibility_branch"),
            min_cgpa=float(data.get("min_cgpa", 0)),
            eligible_year=int(data.get("eligible_year", 0)),
            salary=data.get("salary", ""),
            application_deadline=deadline,
            status="Pending"
        )
        db.session.add(drive)
        db.session.commit()
        cache.delete(f"company_drives_{data.get('company_id')}")  
        cache.delete("admin_all_drives")                           
        return {"message": "Drive created successfully"}, 201
    except Exception as e:
        db.session.rollback()
        import traceback
        traceback.print_exc()
        return {"message": "Failed to create drive", "error": str(e)}, 500


# GET APPLICANTS
def get_applicants(drive_id):
    key = f"drive_applicants_{drive_id}"
    data = cache.get(key)
    if data is None:
        drive = PlacementDrive.query.get(drive_id)
        if not drive:
            return {"message": "Drive not found"}, 404
        applications = Application.query.filter_by(drive_id=drive_id).all()
        data = [{
            "id": app.id,
            "student_id": app.student.id,
            "student_name": app.student.name,
            "roll_no": app.student.roll_no,
            "branch": app.student.branch,
            "cgpa": app.student.cgpa,
            "resume_path": app.student.resume_path,
            "status": app.status
        } for app in applications]
        cache.set(key, data, timeout=120)                         # 2 mins
    return data, 200


# UPDATE APPLICATION STATUS
def update_application_status(application_id, data):
    status = data.get("status")
    if not status:
        return {"message": "status is required"}, 400
    if status not in ["Shortlisted", "Selected", "Rejected"]:
        return {"message": "Invalid status"}, 400
    app = Application.query.get(application_id)
    if not app:
        return {"message": "Application not found"}, 404
    if app.status == "Selected":
        return {"message": "Already selected"}, 400
    if status == "Selected" and app.student.is_placed:
        return {"message": "Student already placed"}, 400
    app.status = status
    if status == "Selected":
        app.student.is_placed = True
    db.session.commit()
    cache.delete(f"drive_applicants_{app.drive_id}")              
    cache.delete(f"student_applications_{app.student_id}")        
    cache.delete("admin_all_applications")                        
    return {"message": f"Application {status}"}, 200


