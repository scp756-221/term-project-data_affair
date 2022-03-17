"""
SFU CMPT 756
Sample application---transaction service.
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
metrics.info('app_info', 'Transaction process')

bp = Blueprint('app', __name__)

db = {
    "name": "http://cmpt756db:30002/api/v1/datastore",
    "endpoint": [
        "read",
        "write",
        "delete",
        "update"
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


@bp.route('/', methods=['GET'])
def list_all():
    """
    Summary line.
  
    Extended description of function.
  
    Parameters:
    arg1 (int): Description of arg1
  
    Returns:
    int: Description of return value
  
    """
    headers = request.headers
    # check header here
    if 'Authorization' not in headers:
        return Response(json.dumps({"error": "missing auth"}),
                        status=401,
                        mimetype='application/json')
    # list all songs here
    return {}


@bp.route('/<transaction_id>', methods=['PUT'])
def update_transaction(transaction_id):
    """
    Summary line.
  
    Extended description of function.
  
    Parameters:
    arg1 (int): Description of arg1
  
    Returns:
    int: Description of return value
  
    """
    headers = request.headers
    # check header here
    if 'Authorization' not in headers:
        return Response(json.dumps({"error": "missing auth"}), status=401,
                        mimetype='application/json')
    try:
        content = request.get_json()
        # TODO update the transaction with fields accordingly
        email = content['email']
        fname = content['fname']
        lname = content['lname']
    except Exception:
        return json.dumps({"message": "error reading arguments"})
    url = db['name'] + '/' + db['endpoint'][3]
    response = requests.put(
        url,
        params={"objtype": "transaction", "objkey": transaction_id},
        json={"email": email, "fname": fname, "lname": lname})
    return (response.json())


@bp.route('/', methods=['POST'])
def create_transaction():
    """
    Create a transaction.
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
        # TODO create the transaction with fields accordingly
        content = request.get_json()
        lname = content['lname']
        email = content['email']
        fname = content['fname']
    except Exception:
        return json.dumps({"message": "error reading arguments"})
    url = db['name'] + '/' + db['endpoint'][1]
    response = requests.post(
        url,
        json={"objtype": "transaction",
              "lname": lname,
              "email": email,
              "fname": fname})
    return (response.json())


@bp.route('/<transaction_id>', methods=['DELETE'])
def delete_transaction(transaction_id):
    """
    Summary line.
  
    Extended description of function.
  
    Parameters:
    arg1 (int): Description of arg1
  
    Returns:
    int: Description of return value
  
    """
    # TODO delete the transaction with fields accordingly
    headers = request.headers
    # check header here
    if 'Authorization' not in headers:
        return Response(json.dumps({"error": "missing auth"}),
                        status=401,
                        mimetype='application/json')
    url = db['name'] + '/' + db['endpoint'][2]

    response = requests.delete(url,
                               params={"objtype": "transaction", "objkey": transaction_id})
    return (response.json())


@bp.route('/<transaction_id>', methods=['GET'])
def get_transaction(transaction_id):
    """
    Summary line.
  
    Extended description of function.
  
    Parameters:
    arg1 (int): Description of arg1
  
    Returns:
    int: Description of return value
  
    """
    # TODO update the transaction with fields accordingly
    headers = request.headers
    # check header here
    if 'Authorization' not in headers:
        return Response(
            json.dumps({"error": "missing auth"}),
            status=401,
            mimetype='application/json')
    payload = {"objtype": "transaction", "objkey": transaction_id}
    url = db['name'] + '/' + db['endpoint'][0]
    response = requests.get(url, params=payload)
    return (response.json())


# @bp.route('/login', methods=['PUT'])
# def login():
#     try:
#         content = request.get_json()
#         uid = content['uid']
#     except Exception:
#         return json.dumps({"message": "error reading parameters"})
#     url = db['name'] + '/' + db['endpoint'][0]
#     response = requests.get(url, params={"objtype": "user", "objkey": uid})
#     data = response.json()
#     if len(data['Items']) > 0:
#         encoded = jwt.encode({'user_id': uid, 'time': time.time()},
#                              'secret',
#                              algorithm='HS256')
#     return encoded


# @bp.route('/logoff', methods=['PUT'])
# def logoff():
#     try:
#         content = request.get_json()
#         _ = content['jwt']
#     except Exception:
#         return json.dumps({"message": "error reading parameters"})
#     return {}


# All database calls will have this prefix.  Prometheus metric
# calls will not---they will have route '/metrics'.  This is
# the conventional organization.
app.register_blueprint(bp, url_prefix='/api/v1/transaction/')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        logging.error("Usage: app.py <service-port>")
        sys.exit(-1)

    p = int(sys.argv[1])
    # Do not set debug=True---that will disable the Prometheus metrics
    app.run(host='0.0.0.0', port=p, threaded=True)
