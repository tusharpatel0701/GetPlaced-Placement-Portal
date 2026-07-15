import os
from urllib.parse import quote_plus

from dotenv import load_dotenv

load_dotenv()

class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #Mail config
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")       
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")       
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_USERNAME")

    # #Celery config
    # CELERY_BROKER_URL = 'redis://localhost:6379/0'
    # CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    # broker_url = 'redis://localhost:6379/0' 
    # result_backend = 'redis://localhost:6379/0' 

    # #Caching config
    # CACHE_TYPE = "RedisCache"
    # CACHE_REDIS_URL = "redis://localhost:6379/1"   
    CACHE_DEFAULT_TIMEOUT = 300                    # 5 minutes default expiry


class LocalDevelopmentConfig(BaseConfig):
    # SQLALCHEMY_DATABASE_URI = "sqlite:///placement_portal.sqlite3"
    # SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:Manish%23%402026@localhost/get_placed_db"

    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = quote_plus(os.getenv("DB_PASSWORD"))

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    SQLALCHEMY_ENGINE_OPTIONS = {
    "connect_args": {
        "ssl": {
            "ca": os.path.join(os.path.dirname(__file__), "ca.pem")
        }
    }
    }

    SECRET_KEY = os.getenv("SECRET_KEY")
    SECURITY_PASSWORD_SALT = os.getenv("SECURITY_PASSWORD_SALT")

class ProductionConfig(BaseConfig):
    DEBUG = False

    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = quote_plus(os.getenv("DB_PASSWORD"))

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    SQLALCHEMY_ENGINE_OPTIONS = {
        "connect_args": {
            "ssl": {
                "ca": os.path.join(os.path.dirname(__file__), "ca.pem")
            }
        }
    }

    SECRET_KEY = os.getenv("SECRET_KEY")
    SECURITY_PASSWORD_SALT = os.getenv("SECURITY_PASSWORD_SALT")

    # Disable Redis cache
    CACHE_TYPE = "NullCache"

    # Disable Celery/Redis
    CELERY_BROKER_URL = None
    CELERY_RESULT_BACKEND = None  