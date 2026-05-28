from flask_restful import Resource
from flask import request
from services.application_services import *


# GET SINGLE APPLICATION
class ApplicationDetail(Resource):
    def get(self, application_id):
        return get_application(application_id)



# UPDATE APPLICATION STATUS
class ApplicationUpdate(Resource):
    def put(self, application_id):
        data = request.get_json()
        return update_application(application_id, data)


# DELETE APPLICATION
class ApplicationDelete(Resource):
    def delete(self, application_id):
        return delete_application(application_id)