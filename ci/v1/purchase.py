"""
Python  API for the purchase service.
"""

# Standard library modules

# Installed packages
from datetime import datetime
import requests


class Purchase():
    """Python API for the purchase service.

    Handles the details of formatting HTTP requests and decoding
    the results.

    Parameters
    ----------
    url: string
        The URL for accessing the purchase service. Often
        'http://cmpt756s3:30010/'. Note the trailing slash.
    auth: string
        Authorization code to pass to the purchase service. For many
        implementations, the code is required but its content is
        ignored.
    """
    def __init__(self, url, auth):
        self._url = url
        self._auth = auth

    def create(self, music_id, user_id, purchase_amount, timestamp=None):
        """Create an artist, song pair.

        Parameters
        ----------
        music_id: string
            The id of the music that was purchased
        user_id: string
            The id of the user who made the purchase
        timestamp: string or None
            The time of the purchase transaction
        purchase_amount: integer
            The price of the music purchased

        Returns
        -------
        (number, string)
            The number is the HTTP status code returned by Purchase.
            The string is the UUID of this purchase transaction in the
            purchase database.
        """
        payload = {'music_id': music_id,
                   'user_id': user_id,
                   'purchase_amount': purchase_amount}
        if timestamp is None:
            payload['time_stamp'] = datetime.now().isoformat()
        else:
            payload['time_stamp'] = timestamp
        r = requests.post(
            self._url,
            json=payload,
            headers={'Authorization': self._auth}
        )
        return r.status_code, r.json()['purchase_id']

    def read(self, p_id):
        """Read details of a purchase.

        Parameters
        ----------
        p_id: string
            The UUID of this purchase in the purchase database.

        Returns
        -------
        music_id, user_id, timestamp, purchase_amount

        music_id: UUID
            The music id for which the purchase is made returned from Purchase.
        user_id: UUID.
          The user id who made the purchase is returned from Purchase.
        timestamp: If status is 200, the timestamp of the song purchase.
          If status is not 200, None.
        purchase_amount: If status is 200, the purchase amount for the song.
          If the status is not 200, None.
        """
        r = requests.get(
            self._url + p_id,
            headers={'Authorization': self._auth}
            )
        if r.status_code != 200:
            return r.status_code, None, None, None, None

        item = r.json()['Items'][0]
        return r.status_code, item['music_id'], item['user_id'], \
            item['time_stamp'], item['purchase_amount']

    def delete(self, p_id):
        """Delete an purchase transaction from the database.

        Parameters
        ----------
        p_id: string
            The UUID of this purchase transaction in the purchase database.

        Returns
        -------
        trc: integer
            The status code of the HTTP call
        """
        r = requests.delete(
            self._url + p_id,
            headers={'Authorization': self._auth}
        )
        return r.status_code

    def update(self, p_id, purchase_amount):
        """Update a transaction from the database.

        Parameters
        ----------
        p_id: string
            The UUID of this purchase transaction in the purchase database.
        purchase_amount: int
            Amount of the transaction

        Returns
        -------
        trc: integer
            The status code of the HTTP call
        """
        r = requests.put(
            self._url + p_id,
            json={'purchase_amount': purchase_amount},
            headers={'Authorization': self._auth}
        )
        return r.status_code

    def get_purchase_by_user(self, u_id):
        """Get all purchases of a user from the purchase database

        Parameters
        ----------
        u_id: string
            The UUID of the user whose purchase is to be retrieved.

        Returns
        -------
        trc: integer
            The status code of the HTTP call

        u_purchases: json object
            The response object containing the keys count - number of items and
            purchases - list of purchases
        """

        r = requests.put(
            self._url + '/byuser/' + u_id,
            headers={'Authorization': self._auth}
        )

        u_purchases = {
            'count': r.json()['Count'],
            'purchases': r.json()['Items']
        }

        return r.status_code, u_purchases
