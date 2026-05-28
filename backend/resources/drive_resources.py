from flask_restful import Resource
from flask import request
from services.drive_services import *


# GET ALL DRIVES
class Drives(Resource):
    def get(self):
        return get_drives(request.args)



# GET SINGLE DRIVE
class DriveDetails(Resource):
    def get(self, drive_id):
        return get_drive_details(drive_id)



# SEARCH DRIVES
class DriveSearch(Resource):
    def get(self):
        keyword = request.args.get("q", "")
        return search_drives(keyword)