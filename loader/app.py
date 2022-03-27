"""
SFU CMPT 756
Loader for sample database
"""

# Standard library modules
from datetime import datetime

import csv
import os
import time
import argparse

# Installed packages
import requests

# The application

loader_token = os.getenv('SVC_LOADER_TOKEN')

# Enough time for Envoy proxy to initialize
# This is only needed if the loader is run with
# Istio injection.  `cluster/loader-tpl.yaml`
# sets that value.
INITIAL_WAIT_SEC = 1

def build_auth():
    """Return a loader Authorization header in Basic format"""
    global loader_token
    return requests.auth.HTTPBasicAuth('svc-loader', loader_token)


def create_user(lname, fname, email, uuid):
    """
    Create a user.
    If a record already exists with the same fname, lname, and email,
    the old UUID is replaced with this one.
    """
    url = db['name'] + '/load'
    response = requests.post(
        url,
        auth=build_auth(),
        json={"objtype": "user",
              "lname": lname,
              "email": email,
              "fname": fname,
              "uuid": uuid})
    return (response.json())


def create_song(artist, title, uuid):
    """
    Create a song.
    If a record already exists with the same artist and title,
    the old UUID is replaced with this one.
    """
    url = db['name'] + '/load'
    response = requests.post(
        url,
        auth=build_auth(),
        json={"objtype": "music",
              "Artist": artist,
              "SongTitle": title,
              "uuid": uuid})
    return (response.json())


def create_purchase(user_id, music_id, purchase_amt, uuid):
    """
    Create a purchase.
    If a record already exists with the same user and music,
    the old UUID is replaced with this one.
    """
    url = db['name'] + '/load'
    response = requests.post(
        url,
        auth=build_auth(),
        json={"objtype": "purchase",
              "user_id": user_id,
              "music_id": music_id,
              "purchase_amount": purchase_amt,
              "timestamp": datetime.now().isoformat(),
              "uuid": uuid})
    return (response.json())


def check_resp(resp, key):
    if 'http_status_code' in resp:
        return None
    else:
        return resp[key]

def parse_args():
    """Parse the command-line arguments.

    Returns
    -------
    db_url
        The url of the DB service
    """
    argp = argparse.ArgumentParser(
        'loader',
        description='Application to load data to dynamodb database'
        )
    argp.add_argument(
        '-D', '--domain',
        help="DNS name or IP address of db service",
        required=False,
        default="cmpt756db"
        )
    argp.add_argument(
        '-P', '--port',
        type=int,
        help="Port number of db service.",
        required=False,
        default="30002"
        )
    args = argp.parse_args()
    db_url = "http://{}:{}/api/v1/datastore".format(
        args.domain, args.port)
    
    return db_url


if __name__ == '__main__':
    # Give Istio proxy time to initialize
    time.sleep(INITIAL_WAIT_SEC)

    resource_dir = 'data'

    db = {
        'name': parse_args() 
    }

    with open('{}/users/users.csv'.format(resource_dir), 'r') as inp:
        rdr = csv.reader(inp)
        next(rdr)  # Skip header
        for fn, ln, email, uuid in rdr:
            resp = create_user(fn.strip(),
                               ln.strip(),
                               email.strip(),
                               uuid.strip())
            resp = check_resp(resp, 'user_id')
            if resp is None or resp != uuid:
                print('Error creating user {} {} ({}), {}'.format(fn,
                                                                  ln,
                                                                  email,
                                                                  uuid))

    with open('{}/music/music.csv'.format(resource_dir), 'r') as inp:
        rdr = csv.reader(inp)
        next(rdr)  # Skip header
        for artist, title, uuid in rdr:
            resp = create_song(artist.strip(),
                               title.strip(),
                               uuid.strip())
            resp = check_resp(resp, 'music_id')
            if resp is None or resp != uuid:
                print('Error creating song {} {}, {}'.format(artist,
                                                             title,
                                                             uuid))

    with open('{}/purchase/purchase.csv'.format(resource_dir), 'r') as inp:
        rdr = csv.reader(inp)
        next(rdr)  # Skip header
        for uuid, user_id, music_id, purchase_amt in rdr:
            resp = create_purchase(user_id,
                               music_id,
                               purchase_amt,
                               uuid)
            resp = check_resp(resp, 'purchase_id')
            if resp is None or resp != uuid:
                print('Error creating purchase {} {}, {}'.format(user_id,
                                                             music_id,
                                                             uuid))

