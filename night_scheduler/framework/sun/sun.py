from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import requests


# https://api.sunrise-sunset.org/json?lat=41.7026974&lng=1.4888376&date=2017-05-23
# https://api.sunrise-sunset.org/json?lat=41.7026974&lng=1.4888376
class Sun(object):
    URL = "https://api.sunrise-sunset.org"

    def __init__(self, date, latitude, longitude):
        self.date = date
        self.latitude = latitude
        self.longitude = longitude

    def get_sunset(self):
        return self._get()["results"]["sunset"]

    def _get(self):
        url = "{}/json?lat={}&lng={}&date={}".format(Sun.URL,
                                                     self.latitude,
                                                     self.longitude,
                                                     self.date)
        return requests.get(url=url)