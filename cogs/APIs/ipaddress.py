"""
IP Address
~~~~~~~~~~


A module that uses https://ip-api.com/
to display info of a IP Address.

"""

import json
import requests

class InvalidIPAddressError(ValueError):
    """A Class that handles error due to 
    invalid IP Address.
    """

    def __init__(self):
        super().__init__('Invalid IP Address.')


def ipinfo(ipaddress: str):
    """A Function that returns a dictionary of
    information on the requested IP Address.
    """

    url = f'http://ip-api.com/json/{ipaddress}'

    req = requests.get(url)

    if req.status_code != requests.codes.ok:
        print('Error Code:',req.status_code)
        return

    info = json.loads(req.text)
    
    if info['status'] != 'fail':
        info.pop('status')
        return info
    else:
        raise InvalidIPAddressError


