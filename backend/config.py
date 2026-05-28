import os
from urllib.parse import quote_plus

class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #Mail config
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")       
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")       
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_USERNAME")

    #Celery config
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    broker_url = 'redis://localhost:6379/0' 
    result_backend = 'redis://localhost:6379/0' 

    #Caching config
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_URL = "redis://localhost:6379/1"   
    CACHE_DEFAULT_TIMEOUT = 300                    # 5 minutes default expiry


class LocalDevelopmentConfig(BaseConfig):
    # SQLALCHEMY_DATABASE_URI = "sqlite:///placement_portal.sqlite3"
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:Manish%23%402026@localhost/get_placed_db"

    SECRET_KEY = os.getenv("SECRET_KEY")
    SECURITY_PASSWORD_SALT = os.getenv("SECURITY_PASSWORD_SALT")

class ProductionConfig(BaseConfig):
    DEBUG = False    