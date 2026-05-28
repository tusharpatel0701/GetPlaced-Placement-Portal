from flask import Blueprint, request, jsonify, current_app
from flask_security.utils import verify_password, hash_password
from models import db, User, Role, Student, Company

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data:
        return jsonify({"message": "No input provided"}), 400

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Invalid input"}), 400

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"message": "User not found"}), 404

    if not verify_password(password, user.password):
        return jsonify({"message": "Wrong password"}), 400
    
    company = Company.query.filter_by(user_id=user.id).first()
    student = Student.query.filter_by(user_id=user.id).first()


    return jsonify({
        "id": user.id,
        "email": user.email,
        "roles": [role.name for role in user.roles],
        "token": user.get_auth_token(),
        "company_id": company.id if company else None,
        "student_id": student.id if student else None
    }), 200



@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if not data:
        return jsonify({"message": "No input provided"}), 400

    email = data.get("email")
    password = data.get("password")
    role_name = data.get("role")

    student_data = data.get("student")
    company_data = data.get("company")

    if not email or not password or not role_name:
        return jsonify({"message": "Missing required fields"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "User already exists"}), 400

    role = Role.query.filter_by(name=role_name).first()
    if not role:
        return jsonify({"message": "Invalid role"}), 400

    datastore = current_app.datastore

    try:
        user = datastore.create_user(
            email=email,
            password=hash_password(password),
            active=True
        )

        datastore.add_role_to_user(user, role)

        db.session.flush()  

        
        if role_name == "student":
            if not student_data:
                return jsonify({"message": "Student data required"}), 400

            student = Student(
                user_id=user.id,
                name=student_data.get("name"),
                roll_no=student_data.get("roll_no"),
                branch=student_data.get("branch"),
                cgpa=student_data.get("cgpa"),
                year=student_data.get("year"),
                phone=student_data.get("phone"),
            )
            db.session.add(student)

      
        elif role_name == "manager":
            if not company_data:
                return jsonify({"message": "Company data required"}), 400

            company = Company(
                user_id=user.id,
                company_name=company_data.get("company_name"),
                website=company_data.get("website"),
                hr_name=company_data.get("hr_name"),
                hr_email=company_data.get("hr_email"),
                hr_phone=company_data.get("hr_phone"),
            )
            db.session.add(company)

    
        db.session.commit()

        return jsonify({
            "id": user.id,
            "email": user.email,
            "role": role.name
        }), 201

    except Exception as e:
        import traceback
        traceback.print_exc()

        db.session.rollback()

        return jsonify({
            "message": "Server error",
            "error": str(e),
            "type": type(e).__name__
        }), 500