from flask import Flask, send_from_directory
from dotenv import load_dotenv
import os

# ✅ Load env FIRST
load_dotenv()

from extension import db, mail, cache
from flask_cors import CORS
from extension import db
from models import *
from config import LocalDevelopmentConfig
from flask_security import Security, SQLAlchemyUserDatastore
from models import User, Role
from resources import auth_bp, api_bp
from celery_worker import make_celery 

def create_app():
    app = Flask(__name__)

    # ✅ Load config
    app.config.from_object(LocalDevelopmentConfig)

    # ✅ Init DB
    db.init_app(app)

    #init mail
    mail.init_app(app)  

    cache.init_app(app)

    # ✅ Setup Flask-Security
    datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, datastore)

    # optional: attach datastore
    app.datastore = datastore


    #blueprint
    app.register_blueprint(auth_bp)

    #flask restful
    # api.init_app(app)
    app.register_blueprint(api_bp)
    

    # ✅ Create tables inside context ONLY
    with app.app_context():
        db.create_all()

    return app


app = create_app()

#create celery instance
celery = make_celery(app) 
CORS(app)

@app.route('/uploads/resumes/<filename>')
def serve_resume(filename):
    upload_folder = os.path.join(os.getcwd(), 'uploads', 'resumes')
    return send_from_directory(upload_folder, filename)

print("BROKER URL:", app.config.get("CELERY_BROKER_URL"))
print("CELERY BROKER:", celery.conf.broker_url)


@app.route("/")
def home():
    return {
        "status": "success",
        "message": "GetPlaced Backend is Running!"
    }, 200

if __name__ == "__main__":
    app.run(debug=True)