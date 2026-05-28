from flask_restful import Resource
from flask import request
from services.admin_services import *


class AdminDashboard(Resource):
    def get(self):
        return get_dashboard_stats()


class AdminStudents(Resource):
    def get(self):
        return get_all_students()


class AdminCompanies(Resource):
    def get(self):
        return get_all_companies()


class AdminCompanyApproval(Resource):
    def put(self, company_id):
        action = request.get_json().get("action")

        if action == "approve":
            return approve_company(company_id)
        elif action == "reject":
            return reject_company(company_id)
        else:
            return {"message": "Invalid action"}, 400


class AdminDrives(Resource):
    def get(self):
        return get_all_drives()


class AdminDriveApproval(Resource):
    def put(self, drive_id):
        action = request.get_json().get("action")

        if action == "approve":
            return approve_drive(drive_id)
        elif action == "reject":
            return reject_drive(drive_id)
        else:
            return {"message": "Invalid action"}, 400


class AdminApplications(Resource):
    def get(self):
        return get_all_applications()


class AdminSearch(Resource):
    def get(self):
        query = request.args.get("q", "")
        return search_entities(query)


class AdminDeactivateUser(Resource):
    def put(self, user_id):
        return deactivate_user(user_id)
    


class TriggerDailyReminder(Resource):
    def post(self):
        return trigger_daily_reminder()

class TriggerMonthlyReport(Resource):
    def post(self):
        return trigger_monthly_report()