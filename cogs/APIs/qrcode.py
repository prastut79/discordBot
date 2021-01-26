"""
Create & Decode QRCode
~~~~~~~~~~~~~~~~~~~~~~


A Module thats uses https://api.qrserver.com/v1/ API
to Create or Decode QrCodes.
"""


import requests
import urllib
import urllib3
import json

class InvalidUrlError(ValueError):
    """A Class that handles error due to 
    invalid URL for Decoding QR Code.
    """
    def __init__(self):
        super().__init__(f"Invalid URL.")


def create_qr(
    data: str,
    height: int = 200,
    width: int = 200,
    color: str = "000",
    bgcolor: str = "fff",
    format: str = "png",
    margin: str = "8",
):
    """A Function to create QRCode.


    It takes the data as the Parameter. 

    It returns the url of the Generated
    QRCode image. 
    """

    info = {
        "size": f"{height}x{width}",
        "data": data,
        "color": color,
        "bgcolor": bgcolor,
        "format": format,
        "margin": margin
    }

    parameters = urllib.parse.urlencode(info)
    url = f"https://api.qrserver.com/v1/create-qr-code/?{parameters}"

    return url


def decode_qr(url: str):
    """A Function to decode QRCode.


    It takes the url of the QRCode image.

    It returns the data of the QRCode image. 
    """

    parsed = (urllib.parse.quote_plus(url))
    url = f'http://api.qrserver.com/v1/read-qr-code/?fileurl={parsed}'

    req = (requests.get(url))
    info = json.loads(req.text)

    if info[0]['symbol'][0]['error'] is None:
        data = info[0]['symbol'][0]['data']
        return data
    else:
        raise InvalidUrlError

