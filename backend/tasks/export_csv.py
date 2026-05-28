import csv
import io
from flask_mail import Message


def export_student_applications(student_id):
    from models import Application, Student, User
    from extension import mail

    student = Student.query.get(student_id)
    if not student:
        return "Student not found"

    user = User.query.get(student.user_id)
    applications = Application.query.filter_by(student_id=student_id).all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "Application ID",
        "Student ID", 
        "Company Name", 
        "Drive Title",
        "Status", 
        "Applied On"
    ])

    for app in applications:
        drive = app.drive
        writer.writerow([
            app.id,
            student_id,
            drive.company.company_name,
            drive.job_title,
            app.status,
            app.application_date.strftime("%Y-%m-%d")
        ])

    csv_data = output.getvalue()

    msg = Message(
        subject="Your Placement Application History",
        recipients=[user.email]
    )
    msg.body = f"Hi {student.name},\n\nYour placement history is attached.\n\n- Placement Cell"
    msg.attach(
        filename="my_applications.csv",
        content_type="text/csv",
        data=csv_data
    )
    mail.send(msg)
    return f"CSV sent to {user.email}"