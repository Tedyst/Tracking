from flask import Blueprint, request, send_file
from Tracking.main import DB, APP
import io
import base64
import uuid


photo_bl = Blueprint("Photo", __name__)
photo_db = DB["photo"]
photourl_db = DB["photourl"]


@photo_bl.route('/admin/<path>')
def admin_path(path):
    result = []
    more_data = photourl_db.find_one({
        "uuid": path
    }, {'_id': False})

    if more_data is not None:
        query = photo_db.find({
            "url": more_data["url"]
        })
    else:
        return {
            "success": False,
            "result": []
        }, 403
    for photo in query:
        if more_data:
            asd = {
                "more_data": True,
                "data": more_data,
                "uuid": path,
                "query": photo["query"],
                "url": photo["url"],
                "ip": photo["ip"]
            }
        else:
            asd = {
                "more_data": False,
                "data": {},
                "uuid": path,
                "query": photo["query"],
                "url": photo["url"],
                "ip": photo["ip"]
            }
        result.append(asd)
    return {
        "success": True,
        "result": result
    }


@photo_bl.route('/create', methods=["POST"])
def create_url():
    data = request.json
    uuid_str = str(uuid.uuid4())
    url_str = str(uuid.uuid4())

    photourl_db.insert({
        "uuid": uuid_str,
        "url": url_str,
        "data": data
    })
    return {
        "uuid": uuid_str,
        "url": url_str
    }


@photo_bl.route('/', defaults={'path': ''})
@photo_bl.route('/<path:path>')
def catch_all(path, **options):
    query = request.query_string.decode('UTF-8')
    url = request.path.replace('/photo/', '').replace('.gif', '')
    ip = request.remote_addr
    photo_db.insert({
        "query": query,
        "url": url,
        "ip": ip
    })
    APP.logger.debug("Opened photo from %s with query %s", ip, query)
    gif = 'R0lGODlhAQABAIAAAP///////yH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=='
    gif_str = base64.b64decode(gif)
    return send_file(io.BytesIO(gif_str), mimetype='image/gif')
