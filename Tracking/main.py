from flask import Flask
from pymongo import MongoClient
import logging
import os
from werkzeug.middleware.proxy_fix import ProxyFix


APP = Flask(__name__)
APP.config['SECRET_KEY'] = os.getenv("SECRET_KEY") or "key"
APP.logger.setLevel(logging.INFO)
APP.wsgi_app = ProxyFix(APP.wsgi_app)
DB = MongoClient('localhost', 27017)["tracking"]
