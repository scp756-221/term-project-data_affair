"""
Python  API for the purchase service.
"""

# Standard library modules

# Installed packages
from datetime import datetime
import requests


class User():
    """Python API for the user service.

    Handles the details of formatting HTTP requests and decoding
    the results.

    Parameters
    ----------
    url: string
        The URL for accessing the purchase service. Often
        'http://cmpt756s1:30000/'. Note the trailing slash.
    auth: string
        Authorization code to pass to the purchase service. For many
        implementations, the code is required but its content is
        ignored.
    """
    def __init__(self, url, auth):
        self._url = url
        self._auth = auth

    def create(self, lname, email, fname):
        """Create a user.

        Parameters
        ----------
        lname: string
            The last name of the new user
        email: string
            The email of the new user
        fname: string or None
            The first name of the user

        Returns
        -------
        (number, string)
            The number is the HTTP status code returned by Purchase.
            The string is the UUID of the user in the User database.
        """
        payload = {'lname': lname,
                   'email': email,
                   'fname': fname}
        r = requests.post(
            self._url,
            json=payload,
            headers={'Authorization': self._auth}
        )
        return r.status_code, r.json()['user_id']
