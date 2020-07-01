from flask import Blueprint, request, send_file
from Tracking.classes import Photo
from Tracking.main import DB, APP
import io
import base64


photo_bl = Blueprint("Photo", __name__)


@photo_bl.route('/admin')
def admin():
    query = Photo.query.all()
    result = []

    for photo in query:
        result.append({
            "ip": photo.ip,
            "url": photo.url,
            "query": str(photo.query_txt),
            "time": photo.time
        })
    return {
        "success": True,
        "result": result
    }


@photo_bl.route('/', defaults={'path': ''})
@photo_bl.route('/<path:path>')
def catch_all(path, **options):
    query = request.query_string
    url = request.path
    ip = request.remote_addr
    photo = Photo(ip, url, query)
    DB.session.add(photo)
    DB.session.commit()
    APP.logger.info("Opened photo from %s with query %s", ip, query)
    gif = 'R0lGODlhAQABAIAAAP///////yH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=='
    gif_str = base64.b64decode(gif)
    return send_file(io.BytesIO(gif_str), mimetype='image/gif')
