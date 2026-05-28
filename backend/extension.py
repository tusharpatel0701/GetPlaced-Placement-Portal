from flask_sqlalchemy import SQLAlchemy
from flask_security.core import Security
from flask_mail import Mail
from flask_caching import Cache 

db = SQLAlchemy()

Security = Security()

mail = Mail()   
cache = Cache()