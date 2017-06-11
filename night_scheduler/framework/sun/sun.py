from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import requests
import time


# https://api.sunrise-sunset.org/json?lat=41.7026974&lng=1.4888376&date=2017-05-23
# https://api.sunrise-sunset.org/json?lat=41.7026974&lng=1.4888376
class Sun(object):
    URL = "https://api.sunrise-sunset.org"

    def __init__(self, date, latitude, longitude):
        self.date = date
        self.latitude = latitude
        self.longitude = longitude

    def get_sunset(self):
        sunset_12h_format_utc = self._get()["results"]["sunset"]
        add_hours = 0
        if "pm" in sunset_12h_format_utc.lower():
            add_hours = 12

        sunset_12h_utc_split = sunset_12h_format_utc[:-2].strip().split(":")
        sunset_24h_format_utc = "{}:{}:{}".format(int(sunset_12h_utc_split[0]) + add_hours,
                                                  sunset_12h_utc_split[1],
                                                  sunset_12h_utc_split[2])

        return self._convert_to_local_time(sunset_24h_format_utc, self.date)

    def _convert_to_local_time(self, utc_time, date):
        # TODO: now this is only for UTC+1 with winter and summer time, correct this with config
        if date.tm_isdst:
            difference = 2
        else:
            difference = 1

        utc_time_split = utc_time.split(":")

        hour = int(utc_time_split[0])+difference
        minute = utc_time_split[1]
        second = utc_time_split[2]

        if hour > 24:
            hour -= 24

        local_time = "{}:{}:{}".format(hour, minute, second)

        return local_time

    def _get(self):
        url = "{}/json?lat={}&lng={}&date={}".format(Sun.URL,
                                                     self.latitude,
                                                     self.longitude,
                                                     "{}-{}-{}".format(self.date.year,
                                                                       self.date.month,
                                                                       self.date.day))
        return requests.get(url=url)
