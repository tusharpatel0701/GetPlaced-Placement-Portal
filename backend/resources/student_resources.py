from flask_restful import Resource
from flask import request
from services.student_services import *


class StudentDrives(Resource):
    def get(self):
        return get_all_approved_drives()


class StudentApply(Resource):
    def post(self, drive_id):
        data = request.get_json()
        return apply_for_drive(drive_id, data)


class StudentApplications(Resource):
    def get(self, student_id):
        return get_student_applications(student_id)


class StudentProfile(Resource):
    def get(self, student_id):
        return get_student_profile(student_id)

    def put(self, student_id):                     
        data = request.get_json()
        return update_student_profile(student_id, data)


class StudentResumeUpload(Resource):
    def post(self, student_id):                   
        return upload_resume(student_id, request.files)


class StudentExportCSV(Resource):
    def post(self, student_id):
        return trigger_csv_export(student_id)