from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import logging
import os
from werkzeug.middleware.proxy_fix import ProxyFix


APP = Flask(__name__)
APP.config['SECRET_KEY'] = os.getenv("SECRET_KEY") or "key"
APP.config['SQLALCHEMY_ECHO'] = False
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
APP.logger.setLevel(logging.INFO)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../data.db'
APP.wsgi_app = ProxyFix(APP.wsgi_app)
DB = SQLAlchemy(APP)
