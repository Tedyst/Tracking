from Tracking.main import APP
import Tracking.classes
from Tracking.modules.photo import photo_bl
from flask import Response

APP.register_blueprint(photo_bl, url_prefix="/photo")



@APP.route('/', defaults={'path': ''})
@APP.route('/<path:path>')
def catch_all(path, **options):
    return Response("404 page not found ", 404, mimetype='text/plain')


if __name__ == "__main__":
    APP.run()
