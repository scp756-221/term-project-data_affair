"""
SFU CMPT 756
Sample application---purchase service.
"""

# Standard library modules
import logging
import sys
import time

# Installed packages
from flask import Blueprint
from flask import Flask
from flask import request
from flask import Response

import jwt

from prometheus_flask_exporter import PrometheusMetrics

import requests

import simplejson as json

# The application

app = Flask(__name__)

metrics = PrometheusMetrics(app)
metrics.info('app_info', 'purchase process')

bp = Blueprint('app', __name__)

db = {
    "name": "http://cmpt756db:30002/api/v1/datastore",
    "endpoint": [
        "read",
        "write",
        "delete",
        "update",
        "fetch"
    ]
}


# @bp.route('/', methods=['GET'])
# @metrics.do_not_track()
# def hello_world():
#     return ("If you are reading this in a browser, your service is "
#             "operational. Switch to curl/Postman/etc to interact using the "
#             "other HTTP verbs.")


@bp.route('/health')
@metrics.do_not_track()
def health():
    return Response("", status=200, mimetype="application/json")


@bp.route('/readiness')
@metrics.do_not_track()
def readiness():
    return Response("", status=200, mimetype="application/json")



@bp.route('/', methods=['PUT'])
def update_purchase():
    """
    Summary line:
        Updates the purchases table, whenever an exchange is carried out
  
    Parameters:
        Null
  
    Returns:
        The response for updated purchase.
  
    """
    headers = request.headers
    # check header here
    if 'Authorization' not in headers:
        return Response(json.dumps({"error": "missing auth"}), status=401,
                        mimetype='application/json')
    try:
        content = request.get_json()
        # TODO update the purchase with fields accordingly
        purchase_id = content['purchase_id']
        music_id = content['music_id']
        user_id = content['user_id']
        timestamp = datetime.now().isoformat()
        purchase_amount = content['purchase_amount']
    except Exception:
        return json.dumps({"message": "error reading arguments"})
    url = db['name'] + '/' + db['endpoint'][3]
    response = requests.put(
        url,
        params={"objtype": "purchase", "objkey": purchase_id},
        json={"purchase_id": purchase_id, "music_id": music_id,
              "user_id": user_id, "time_stamp":timestamp, "purchase_amount": purchase_amount },
        headers={'Authorization': headers['Authorization']})
    return (response.json())

@bp.route('/', methods=['POST'])
def create_purchase():
    """
    Create a purchase.
    If a record already exists with the same fname, lname, and email,
    the old UUID is replaced with a new one.
  
    Parameters:
    arg1 (int): Description of arg1
  
    Returns:
    int: Description of return value
  
    """
    """
    
    """
    try:
        # TODO create the purchase with fields accordingly
        content = request.get_json()
        music_id = content['music_id']
        user_id = content['user_id']
        timestamp = datetime.now().isoformat()
        purchase_amount = content['purchase_amount']
    except Exception:
        return json.dumps({"message": "error reading arguments"})
    url = db['name'] + '/' + db['endpoint'][1]
    response = requests.post(
        url,
        json={"objtype": "purchase",
              "music_id": music_id,
              "user_id": user_id,
              "time_stamp": timestamp,
              "purchase_amount": purchase_amount
            })
    return (response.json())


@bp.route('/<purchase_id>', methods=['DELETE'])
def delete_purchase(purchase_id):
    """
    Summary line.
  
    Extended description of function.
  
    Parameters:
    arg1 (int): Description of arg1
  
    Returns:
    int: Description of return value
  
    """
    # TODO delete the purchase with fields accordingly
    headers = request.headers
    # check header here
    if 'Authorization' not in headers:
        return Response(json.dumps({"error": "missing auth"}),
                        status=401,
                        mimetype='application/json')
    url = db['name'] + '/' + db['endpoint'][2]

    response = requests.delete(url,
                               params={"objtype": "purchase", "objkey": purchase_id})
    return (response.json())


@bp.route('/<purchase_id>', methods=['GET'])
def get_purchase(purchase_id):
    """
    Get details of a single purchase by purchase id.
  
    Parameters:
    purchase_id (int): purchase id
  
    Returns:
    obj: purchase details for purchase given by purchase_id
  
    """
    headers = request.headers
    # check header here
    if 'Authorization' not in headers:
        return Response(
            json.dumps({"error": "missing auth"}),
            status=401,
            mimetype='application/json')
    payload = {"objtype": "purchase", "objkey": purchase_id}
    url = db['name'] + '/' + db['endpoint'][0]
    response = requests.get(url, params=payload)
    return (response.json())

@bp.route('/byuser/<user_id>', methods=['GET'])
def get_purchase_by_user(user_id):
    """
    Get details of purchases by user id.
  
    Parameters:
    user_id (int): user id
  
    Returns:
    obj: purchase details for purchases given by user id
  
    """
    headers = request.headers
    # check header here
    if 'Authorization' not in headers:
        return Response(
            json.dumps({"error": "missing auth"}),
            status=401,
            mimetype='application/json')
    payload = {"objtype": "purchase", "objkey": user_id, "keytype": "user"}
    url = db['name'] + '/' + db['endpoint'][4]
    response = requests.get(url, params=payload)
    return (response.json())

# All database calls will have this prefix.  Prometheus metric
# calls will not---they will have route '/metrics'.  This is
# the conventional organization.
app.register_blueprint(bp, url_prefix='/api/v1/purchase/')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        logging.error("Usage: app.py <service-port>")
        sys.exit(-1)

    p = int(sys.argv[1])
    # Do not set debug=True---that will disable the Prometheus metrics
    app.run(host='0.0.0.0', port=p, threaded=True)
