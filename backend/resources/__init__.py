from flask_restful import Api
from flask import Blueprint

from resources.application_resources import *
from resources.company_resources import *
from resources.student_resources import *
from resources.admin_resources import *
from resources.drive_resources import *

from resources.auth_resources import auth_bp 

api_bp = Blueprint("api", __name__, "/api")

api = Api(api_bp)

api.add_resource(AdminDashboard, "/api/admin/dashboard")

api.add_resource(AdminStudents, "/api/admin/students")

api.add_resource(AdminCompanies, "/api/admin/companies")

api.add_resource(AdminCompanyApproval, "/api/admin/company/<int:company_id>")

api.add_resource(AdminDrives, "/api/admin/drives")

api.add_resource(AdminDriveApproval, "/api/admin/drive/<int:drive_id>")

api.add_resource(AdminApplications, "/api/admin/applications")

api.add_resource(AdminSearch, "/api/admin/search")

api.add_resource(AdminDeactivateUser, "/api/admin/user/<int:user_id>/deactivate") 

api.add_resource(TriggerDailyReminder, "/api/admin/trigger-reminder")
api.add_resource(TriggerMonthlyReport, "/api/admin/trigger-monthly-report")


#Student Resources
api.add_resource(StudentDrives, "/api/student/drives")

api.add_resource(StudentApply, "/api/student/apply/<int:drive_id>")

api.add_resource(StudentApplications, "/api/student/applications/<int:student_id>")

api.add_resource(StudentProfile, "/api/student/profile/<int:student_id>")

api.add_resource(StudentResumeUpload, "/api/student/resume/<int:student_id>")

api.add_resource(StudentExportCSV, "/api/student/<int:student_id>/export-csv")


#drive resources
api.add_resource(Drives, "/api/drives")

api.add_resource(DriveDetails, "/api/drives/<int:drive_id>")

api.add_resource(DriveSearch, "/api/drives/search")


#company resources
api.add_resource(CompanyProfile, "/api/company/profile/<int:company_id>")

api.add_resource(CompanyCreateDrive, "/api/company/create-drive")

api.add_resource(CompanyDrives, "/api/company/drives/<int:company_id>")

api.add_resource(CompanyApplicants, "/api/company/applicants/<int:drive_id>")

api.add_resource(CompanyUpdateApplication, "/api/company/application/<int:application_id>")


#application resources
api.add_resource(ApplicationDetail, "/api/application/<int:application_id>")

api.add_resource(ApplicationUpdate, "/api/application/<int:application_id>/update")

api.add_resource(ApplicationDelete, "/api/application/<int:application_id>/delete")