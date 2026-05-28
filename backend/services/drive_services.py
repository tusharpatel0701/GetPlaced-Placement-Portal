from models import PlacementDrive



# GET ALL DRIVES (WITH FILTERS)
def get_drives(query_params):
    drives_query = PlacementDrive.query.filter_by(status="Approved")

    branch = query_params.get("branch")
    min_cgpa = query_params.get("cgpa")
    year = query_params.get("year")

    if branch:
        drives_query = drives_query.filter(
            PlacementDrive.eligibility_branch == branch
        )

    if min_cgpa:
        drives_query = drives_query.filter(
            PlacementDrive.min_cgpa <= float(min_cgpa)
        )

    if year:
        drives_query = drives_query.filter(
            PlacementDrive.eligible_year == int(year)
        )

    drives = drives_query.all()

    return [{
        "id": d.id,
        "company": d.company.company_name,
        "job_title": d.job_title,
        "salary": d.salary,
        "min_cgpa": d.min_cgpa,
        "eligible_year": d.eligible_year,
        "branch": d.eligibility_branch,
        "deadline": d.application_deadline.strftime("%Y-%m-%d"),
        "status": d.status
    } for d in drives], 200



# GET SINGLE DRIVE
def get_drive_details(drive_id):
    drive = PlacementDrive.query.get(drive_id)

    if not drive:
        return {"message": "Drive not found"}, 404

    return {
        "id": drive.id,
        "company": drive.company.company_name,
        "job_title": drive.job_title,
        "job_description": drive.job_description,
        "salary": drive.salary,
        "min_cgpa": drive.min_cgpa,
        "eligible_year": drive.eligible_year,
        "branch": drive.eligibility_branch,
        "deadline": drive.application_deadline.strftime("%Y-%m-%d"),
        "status": drive.status
    }, 200


# SEARCH DRIVES
def search_drives(keyword):
    if not keyword:
        return [], 200

    drives = PlacementDrive.query.filter(
        PlacementDrive.job_title.ilike(f"%{keyword}%")
    ).all()

    return [{
        "id": d.id,
        "company": d.company.company_name,
        "job_title": d.job_title,
        "deadline": d.application_deadline.strftime("%Y-%m-%d")
    } for d in drives], 200