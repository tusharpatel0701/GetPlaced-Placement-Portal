# from models import User, Student, Company, PlacementDrive, Application, db
# from extension import cache


# # DASHBOARD STATS
# def get_dashboard_stats():
#     return {
#         "total_students": Student.query.count(),
#         "total_companies": Company.query.count(),
#         "total_drives": PlacementDrive.query.count()
#     }, 200


# # GET ALL STUDENTS
# def get_all_students():
#     students = Student.query.all()

#     result = []
#     for s in students:
#         result.append({
#             "id": s.id,
#             "name": s.name,
#             "email": s.user.email if s.user else "N/A",
#             "status": "Active" if s.user and s.user.active else "Blacklisted"
#         })

#     return result, 200


# # GET ALL COMPANIES
# def get_all_companies():
#     companies = Company.query.all()

#     result = []
#     for c in companies:
#         result.append({
#             "id": c.id,
#             "company_name": c.company_name,
#             "approval_status": c.approval_status,
#             "hr_email": c.hr_email
#         })

#     return result, 200


# # APPROVE COMPANY
# def approve_company(company_id):
#     company = Company.query.get(company_id)

#     if not company:
#         return {"message": "Company not found"}, 404

#     company.approval_status = "Approved"

#     # ✅ Use direct column update instead of property setter
#     User.query.filter_by(id=company.user_id).update({"active": True})

#     db.session.commit()

#     return {"message": "Company approved"}, 200


# # REJECT COMPANY
# def reject_company(company_id):
#     company = Company.query.get(company_id)

#     if not company:
#         return {"message": "Company not found"}, 404

#     company.approval_status = "Rejected"

#     # ✅ Use direct column update instead of property setter
#     User.query.filter_by(id=company.user_id).update({"active": False})

#     db.session.commit()

#     return {"message": "Company rejected"}, 200


# # GET ALL DRIVES
# def get_all_drives():
#     drives = PlacementDrive.query.all()

#     result = []
#     for d in drives:
#         result.append({
#             "id": d.id,
#             "company": d.company.company_name,
#             "job_title": d.job_title,
#             "status": d.status,
#             "deadline": d.application_deadline.strftime("%Y-%m-%d") if d.application_deadline else None
#         })

#     return result, 200


# # APPROVE DRIVE
# def approve_drive(drive_id):
#     drive = PlacementDrive.query.get(drive_id)

#     if not drive:
#         return {"message": "Drive not found"}, 404

#     drive.status = "Approved"

#     db.session.commit()

#     return {"message": "Drive approved"}, 200


# # REJECT DRIVE
# def reject_drive(drive_id):
#     drive = PlacementDrive.query.get(drive_id)

#     if not drive:
#         return {"message": "Drive not found"}, 404

#     drive.status = "Rejected"

#     db.session.commit()

#     return {"message": "Drive rejected"}, 200



# # GET ALL APPLICATIONS
# def get_all_applications():
#     applications = Application.query.order_by(Application.application_date.desc()).all()

#     result = []
#     for a in applications:
#         result.append({
#             "id": a.id,
#             "student_name": a.student.name if a.student else "N/A",
#             "company": a.drive.company.company_name if a.drive and a.drive.company else "N/A",
#             "job_title": a.drive.job_title if a.drive else "N/A",
#             "status": a.status,
#             "applied_on": a.application_date.strftime("%Y-%m-%d") if a.application_date else None
#         })

#     return result, 200


# # SEARCH
# def search_entities(query):
#     if not query:
#         return {"students": [], "companies": []}, 200

#     students = Student.query.filter(Student.name.ilike(f"%{query}%")).all()
#     companies = Company.query.filter(Company.company_name.ilike(f"%{query}%")).all()

#     return {
#         "students": [
#             {"id": s.id, "name": s.name}
#             for s in students
#         ],
#         "companies": [
#             {"id": c.id, "company_name": c.company_name}
#             for c in companies
#         ]
#     }, 200


# # ==========================
# # DEACTIVATE USER
# # ==========================

# def deactivate_user(user_id):
#     student = Student.query.get(user_id)

#     if not student:
#         return {"message": "User not found"}, 404

#     student.user.active = False
#     db.session.commit()

#     return {"message": "User blacklisted"}, 200


# def trigger_daily_reminder():
#     from app import celery
#     task = celery.send_task("tasks.reminders.send_daily_reminders")
#     return {"message": "Daily reminders sent successfully!", "task_id": task.id}, 202

# def trigger_monthly_report():
#     from app import celery
#     task = celery.send_task("tasks.monthly_report.send_monthly_report")
#     return {"message": "Monthly report sent to admin email!", "task_id": task.id}, 202











from models import User, Student, Company, PlacementDrive, Application, db                      


# DASHBOARD STATS
def get_dashboard_stats():
    # data = cache.get("admin_dashboard_stats")
    # if data is None:                                
    data = {
            "total_students": Student.query.count(),
            "total_companies": Company.query.count(),
            "total_drives": PlacementDrive.query.count()
        }
        # cache.set("admin_dashboard_stats", data, timeout=300)  
    return data, 200


# GET ALL STUDENTS
def get_all_students():
    # data = cache.get("admin_all_students")
    # if data is None:
    students = Student.query.all()
    data = [{
            "id": s.id,
            "name": s.name,
            "email": s.user.email if s.user else "N/A",
            "status": "Active" if s.user and s.user.active else "Blacklisted"
        } for s in students]
        # cache.set("admin_all_students", data, timeout=180)     # 3 mins
    return data, 200


# GET ALL COMPANIES
def get_all_companies():
    #data = cache.get("admin_all_companies")
    # if data is None:
    companies = Company.query.all()
    data = [{
            "id": c.id,
            "company_name": c.company_name,
            "approval_status": c.approval_status,
            "hr_email": c.hr_email
        } for c in companies]
        # cache.set("admin_all_companies", data, timeout=180)    # 3 mins
    return data, 200


# GET ALL DRIVES
def get_all_drives():
    # data = cache.get("admin_all_drives")
    # if data is None:
    drives = PlacementDrive.query.all()
    data = [{
            "id": d.id,
            "company": d.company.company_name,
            "job_title": d.job_title,
            "status": d.status,
            "deadline": d.application_deadline.strftime("%Y-%m-%d") if d.application_deadline else None
        } for d in drives]
        # cache.set("admin_all_drives", data, timeout=180)       # 3 mins
    return data, 200


# GET ALL APPLICATIONS
def get_all_applications():
    # data = cache.get("admin_all_applications")
    # if data is None:
    applications = Application.query.order_by(Application.application_date.desc()).all()
    data = [{
            "id": a.id,
            "student_name": a.student.name if a.student else "N/A",
            "company": a.drive.company.company_name if a.drive and a.drive.company else "N/A",
            "job_title": a.drive.job_title if a.drive else "N/A",
            "status": a.status,
            "applied_on": a.application_date.strftime("%Y-%m-%d") if a.application_date else None
        } for a in applications]
        # cache.set("admin_all_applications", data, timeout=120) # 2 mins
    return data, 200


# APPROVE COMPANY
def approve_company(company_id):
    company = Company.query.get(company_id)
    if not company:
        return {"message": "Company not found"}, 404
    company.approval_status = "Approved"
    User.query.filter_by(id=company.user_id).update({"active": True})
    db.session.commit()
    # cache.delete("admin_all_companies")                        # ✅ clear
    # cache.delete("admin_dashboard_stats")                      # ✅ clear
    return {"message": "Company approved"}, 200


# REJECT COMPANY
def reject_company(company_id):
    company = Company.query.get(company_id)
    if not company:
        return {"message": "Company not found"}, 404
    company.approval_status = "Rejected"
    User.query.filter_by(id=company.user_id).update({"active": False})
    db.session.commit()
    # cache.delete("admin_all_companies")                       
    # cache.delete("admin_dashboard_stats")                      
    return {"message": "Company rejected"}, 200


# APPROVE DRIVE
def approve_drive(drive_id):
    drive = PlacementDrive.query.get(drive_id)
    if not drive:
        return {"message": "Drive not found"}, 404
    drive.status = "Approved"
    db.session.commit()
    # cache.delete("admin_all_drives")                           
    # cache.delete("student_approved_drives")                    
    return {"message": "Drive approved"}, 200


# REJECT DRIVE
def reject_drive(drive_id):
    drive = PlacementDrive.query.get(drive_id)
    if not drive:
        return {"message": "Drive not found"}, 404
    drive.status = "Rejected"
    db.session.commit()
    # cache.delete("admin_all_drives")                           
    # cache.delete("student_approved_drives")                    
    return {"message": "Drive rejected"}, 200


# DEACTIVATE USER
def deactivate_user(user_id):
    student = Student.query.get(user_id)
    if not student:
        return {"message": "User not found"}, 404
    student.user.active = False
    db.session.commit()
    # cache.delete("admin_all_students")                         
    # cache.delete("admin_dashboard_stats")                      
    return {"message": "User blacklisted"}, 200



# SEARCH — students, companies AND drives
def search_entities(query):
    if not query:
        return {"students": [], "companies": [], "drives": []}, 200

    students = Student.query.filter(
        Student.name.ilike(f"%{query}%")
    ).all()

    companies = Company.query.filter(
        Company.company_name.ilike(f"%{query}%")
    ).all()

    drives = PlacementDrive.query.filter(         
        PlacementDrive.job_title.ilike(f"%{query}%")
    ).all()

    return {
        "students": [{"id": s.id, "name": s.name} for s in students],
        "companies": [{"id": c.id, "company_name": c.company_name} for c in companies],
        "drives": [                               
            {
                "id": d.id,
                "job_title": d.job_title,
                "company_name": d.company.company_name
            } for d in drives
        ]
    }, 200


# SEARCH 
def search_entities(query):
    if not query:
        return {"students": [], "companies": []}, 200
    students = Student.query.filter(Student.name.ilike(f"%{query}%")).all()
    companies = Company.query.filter(Company.company_name.ilike(f"%{query}%")).all()
    return {
        "students": [{"id": s.id, "name": s.name} for s in students],
        "companies": [{"id": c.id, "company_name": c.company_name} for c in companies]
    }, 200


def trigger_daily_reminder():
    from app import celery
    task = celery.send_task("tasks.reminders.send_daily_reminders")
    return {"message": "Daily reminders sent successfully!", "task_id": task.id}, 202


def trigger_monthly_report():
    from app import celery
    task = celery.send_task("tasks.monthly_report.send_monthly_report")
    return {"message": "Monthly report sent to admin email!", "task_id": task.id}, 202