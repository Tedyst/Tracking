from Tracking.main import DB
import time


class Photo(DB.Model):
    __tablename__ = "photo"
    id = DB.Column(DB.Integer, primary_key=True)
    query_txt = DB.Column(DB.String(50))
    ip = DB.Column(DB.String(15))
    time = DB.Column(DB.Integer())

    def __init__(self, ip, query):
        self.query_txt = str(query)
        self.ip = ip
        self.time = int(time.time())

DB.create_all()