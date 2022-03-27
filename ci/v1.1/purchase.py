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
            The string is the UUID of this purchase transaction in the purchase database.
        """
        payload = {'music_id': music_id,
                   'user_id': user_id,
                   'purchase_amount': purchase_amount}
        if timestamp is None:
            payload['timestamp'] = datetime.now().isoformat()
        else:
            payload['timestamp'] = timestamp
        r = requests.post(
            self._url,
            json=payload,
            headers={'Authorization': self._auth}
        )
        return r.status_code, r.json()['purchase_id']

    # TODO change accordingly for update_purchase() api in purchase service
    def write_orig_artist(self, m_id, orig_artist):
        """Write the original artist performing a song.

        Parameters
        ----------
        m_id: string
            The UUID of this song in the purchase database.

        orig_artist: string
            The original artist performing the song.

        Returns
        -------
        number
            The HTTP status code returned by the purchase service.
        """
        r = requests.put(
            self._url + 'write_orig_artist/' + m_id,
            json={'OrigArtist': orig_artist},
            headers={'Authorization': self._auth}
        )
        return r.status_code

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
        return r.status_code, item['music_id'], item['user_id'], item['timestamp'], item['purchase_amount']

    # TODO change accordingly for get_purchase_by_user() api in purchase service
    def read_orig_artist(self, m_id):
        """Read the orginal artist of a song.

        Parameters
        ----------
        m_id: string
            The UUID of this song in the purchase database.

        Returns
        -------
        status, orig_artist

        status: number
            The HTTP status code returned by Purchase.
        orig_artist:
          If status is 200, the original artist who
            performed the song.
          If status is not 200, None.
        """
        r = requests.get(
            self._url + 'read_orig_artist/' + m_id,
            headers={'Authorization': self._auth}
            )
        if r.status_code != 200:
            return r.status_code, None
        item = r.json()
        return r.status_code, item['OrigArtist']

    # TODO change accordingly for delete_purchase() api in purchase service
    def delete(self, p_id):
        """Delete an transaction from the database.

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