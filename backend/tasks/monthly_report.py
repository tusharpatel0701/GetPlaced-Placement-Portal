from flask_mail import Message
from datetime import datetime, timezone


def send_monthly_report():
    from models import PlacementDrive, Application, User
    from extension import mail, db

    now = datetime.now(timezone.utc)
    last_month = now.month - 1 if now.month > 1 else 12
    year = now.year if now.month > 1 else now.year - 1

    drives = PlacementDrive.query.filter(
        db.extract("month", PlacementDrive.created_at) == last_month,
        db.extract("year", PlacementDrive.created_at) == year
    ).all()

    total_drives = len(drives)
    drive_ids = [d.id for d in drives]
    all_apps = Application.query.filter(
        Application.drive_id.in_(drive_ids)
    ).all() if drive_ids else []

    total_applied = len(all_apps)
    total_selected = len([a for a in all_apps if a.status == "Selected"])
    month_name = datetime(year, last_month, 1).strftime("%B %Y")

    rows = ""
    for drive in drives:
        apps = [a for a in all_apps if a.drive_id == drive.id]
        selected = len([a for a in apps if a.status == "Selected"])
        rows += f"<tr><td>{drive.company.company_name}</td><td>{drive.job_title}</td><td>{len(apps)}</td><td>{selected}</td></tr>"

    html = f"""
    <html><body style="font-family: Arial, sans-serif; padding: 20px;">
        <h2>Monthly Placement Report — {month_name}</h2>
        <table border="1" cellpadding="10" cellspacing="0" style="border-collapse:collapse;">
            <tr style="background:#f0f0f0;"><th>Metric</th><th>Count</th></tr>
            <tr><td>Total Drives Conducted</td><td>{total_drives}</td></tr>
            <tr><td>Total Students Applied</td><td>{total_applied}</td></tr>
            <tr><td>Total Students Selected</td><td>{total_selected}</td></tr>
        </table>
        <br>
        <h3>Drive-wise Breakdown</h3>
        <table border="1" cellpadding="10" cellspacing="0" style="border-collapse:collapse;">
            <tr style="background:#f0f0f0;"><th>Company</th><th>Job Title</th><th>Applicants</th><th>Selected</th></tr>
            {rows if rows else "<tr><td colspan='4'>No drives this month</td></tr>"}
        </table>
        <p style="color:gray;">Generated on {now.strftime('%d %B %Y')}</p>
    </body></html>
    """

    admin = User.query.join(User.roles).filter_by(name="admin").first()
    if not admin:
        return "Admin not found!"

    msg = Message(subject=f"Monthly Placement Report — {month_name}", recipients=[admin.email])
    msg.html = html
    mail.send(msg)
    return f"Monthly report sent to {admin.email}"