from celery import Celery
from celery.schedules import crontab


def make_celery(app):
    celery = Celery("app")

    celery.conf.update(
        broker_url="redis://localhost:6379/0",
        result_backend="redis://localhost:6379/0",
        task_serializer="json",
        accept_content=["json"],
        result_serializer="json",
        timezone="Asia/Kolkata",
        enable_utc=True,
        beat_schedule={
            "daily-reminders": {
                "task": "tasks.reminders.send_daily_reminders",
                "schedule": crontab(hour=9, minute=0),
            },
            "monthly-report": {
                "task": "tasks.monthly_report.send_monthly_report",
                "schedule": crontab(day_of_month=1, hour=8, minute=0),
            },
        }
    )

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask

    # Register tasks manually using the celery instance
    from tasks import reminders, monthly_report, export_csv

    celery.task(name="tasks.reminders.send_daily_reminders")(reminders.send_daily_reminders)
    celery.task(name="tasks.monthly_report.send_monthly_report")(monthly_report.send_monthly_report)
    celery.task(name="tasks.export_csv.export_student_applications")(export_csv.export_student_applications)

    return celery