from flask_restful import Resource
from flask import request
from services.company_services import *


#GET COMPANY PROFILE
class CompanyProfile(Resource):
    def get(self, company_id):
        return get_company_profile(company_id)

# CREATE PLACEMENT DRIVE
class CompanyCreateDrive(Resource):
    def post(self):
        data = request.get_json()
        return create_drive(data)



# VIEW COMPANY DRIVES
class CompanyDrives(Resource):
    def get(self, company_id):
        return get_company_drives(company_id)


# VIEW APPLICANTS
class CompanyApplicants(Resource):
    def get(self, drive_id):
        return get_applicants(drive_id)


# UPDATE APPLICATION STATUS
class CompanyUpdateApplication(Resource):
    def put(self, application_id):
        data = request.get_json()
        return update_application_status(application_id, data)