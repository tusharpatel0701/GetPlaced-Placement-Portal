from models import Application, db



# GET SINGLE APPLICATION
def get_application(application_id):
    app = Application.query.get(application_id)

    if not app:
        return {"message": "Application not found"}, 404

    return {
        "id": app.id,
        "student_id": app.student.id,
        "student_name": app.student.name,
        "company": app.drive.company.company_name,
        "job_title": app.drive.job_title,
        "status": app.status,
        "applied_on": app.application_date.strftime("%Y-%m-%d")
    }, 200



# UPDATE APPLICATION STATUS
def update_application(application_id, data):
    status = data.get("status")

    if not status:
        return {"message": "status is required"}, 400

    valid_status = ["Applied", "Shortlisted", "Selected", "Rejected"]

    if status not in valid_status:
        return {"message": "Invalid status"}, 400

    app = Application.query.get(application_id)

    if not app:
        return {"message": "Application not found"}, 404

    # prevent overriding final state
    if app.status == "Selected":
        return {"message": "Already finalized"}, 400

    app.status = status

    # mark student placed if selected
    if status == "Selected":
        app.student.is_placed = True

    db.session.commit()

    return {"message": f"Application updated to {status}"}, 200



# DELETE APPLICATION
def delete_application(application_id):
    app = Application.query.get(application_id)

    if not app:
        return {"message": "Application not found"}, 404

    db.session.delete(app)
    db.session.commit()

    return {"message": "Application deleted"}, 200