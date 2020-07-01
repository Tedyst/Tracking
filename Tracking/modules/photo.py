from flask import Blueprint, request, send_file
from Tracking.classes import Photo, PhotoURL
from Tracking.main import DB, APP
import io
import base64
import uuid
import json


photo_bl = Blueprint("Photo", __name__)


@photo_bl.route('/admin/<path>')
def admin_path(path):
    query = Photo.query.filter(Photo.url == path).all()
    result = []

    for photo in query:
        asd = {
            "more_data": False,
            "data": {}
        }
        more_data = PhotoURL.query.filter(PhotoURL.url == photo.url).first()
        if more_data is not None:
            asd["data"].update(json.loads(more_data.data))
            asd["more_data"] = True
        asd.update({
            "ip": photo.ip,
            "url": photo.url,
            "query": str(photo.query_txt),
            "time": photo.time
        })
        result.append(asd)
    return {
        "success": True,
        "result": result
    }


@photo_bl.route('/admin')
def admin():
    query = Photo.query.all()
    result = []

    for photo in query:
        asd = {
            "more_data": False,
            "data": {}
        }
        more_data = PhotoURL.query.filter(PhotoURL.url == photo.url).first()
        if more_data is not None:
            asd["data"].update(json.loads(more_data.data))
            asd["more_data"] = True
        asd.update({
            "ip": photo.ip,
            "url": photo.url,
            "query": str(photo.query_txt),
            "time": photo.time
        })
        result.append(asd)
    return {
        "success": True,
        "result": result
    }


@photo_bl.route('/create', methods=["POST"])
def create_url():
    data = str(request.data.decode('UTF-8'))
    uuid_str = str(uuid.uuid4())
    saved = PhotoURL(uuid_str, data)
    DB.session.add(saved)
    DB.session.commit()
    return {
        "uuid": uuid_str
    }


@photo_bl.route('/', defaults={'path': ''})
@photo_bl.route('/<path:path>')
def catch_all(path, **options):
    query = request.query_string.decode('UTF-8')
    url = request.path.replace('/photo/', '').replace('.gif', '')
    ip = request.remote_addr
    photo = Photo(ip, url, query)
    DB.session.add(photo)
    DB.session.commit()
    APP.logger.info("Opened photo from %s with query %s", ip, query)
    gif = 'R0lGODlhAQABAIAAAP///////yH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=='
    gif_str = base64.b64decode(gif)
    return send_file(io.BytesIO(gif_str), mimetype='image/gif')
