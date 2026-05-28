from flask_mail import Message
from datetime import datetime, timedelta, timezone


def send_daily_reminders():
    from models import PlacementDrive, Application, Student, User
    from extension import mail

    today = datetime.now(timezone.utc).date()
    three_days_later = today + timedelta(days=3)

    upcoming_drives = PlacementDrive.query.filter(
        PlacementDrive.status == "Approved",
        PlacementDrive.application_deadline >= today,
        PlacementDrive.application_deadline <= three_days_later
    ).all()

    count = 0
    for drive in upcoming_drives:
        already_applied_ids = [
            a.student_id for a in
            Application.query.filter_by(drive_id=drive.id).all()
        ]
        eligible_students = Student.query.filter(
            Student.id.notin_(already_applied_ids)
        ).all()

        for student in eligible_students:
            user = User.query.get(student.user_id)
            if not user or not user.active:
                continue
            msg = Message(
                subject=f"Reminder: Apply for {drive.job_title} before deadline!",
                recipients=[user.email]
            )
            msg.body = f"""
Hi {student.name},

The drive for "{drive.job_title}" by {drive.company.company_name}
closes on {drive.application_deadline}. Login and apply now!

- Placement Cell
            """
            mail.send(msg)
            count += 1

    return f"Sent {count} reminder emails."