from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import pytest
import datetime

from mock import patch

from night_scheduler.framework.sun.sun import Sun


class FakeDateTime(object):
    def __init__(self):
        self.year = 9999
        self.month = 1
        self.day = 1
        self.tm_isdst = 1

    def set_summer(self):
        self.tm_isdst = 1

    def set_winter(self):
        self.tm_isdst = 0


class TestSunShoud(object):
    FAKE_LATITUDE = "00"
    FAKE_LONGITUDE = "11"
    FAKE_SUNSET_SUMMER = "21:00:00"
    FAKE_SUNSET_WINTER = "20:00:00"
    FAKE_SUNRISE_SUNSERT_ORG_ANSWER = {
        "results": {
            "sunrise": "4:26:42 AM",
            "sunset": "7:00:00 PM",
            "solar_noon": "11:50:51 AM",
            "day_length": "14:48:18",
            "civil_twilight_begin": "3:54:08 AM",
            "civil_twilight_end": "7:47:34 PM",
            "nautical_twilight_begin": "3:12:59 AM",
            "nautical_twilight_end": "8:28:43 PM",
            "astronomical_twilight_begin": "2:25:39 AM",
            "astronomical_twilight_end": "9:16:04 PM"
        },
        "status": "OK"
    }

    @classmethod
    def setup_method(self, method):
        self.patcher_requests_get = patch('requests.get')

        self.mock_requests_get = self.patcher_requests_get.start()
        self.mock_requests_get.return_value = TestSunShoud.FAKE_SUNRISE_SUNSERT_ORG_ANSWER

        self.fake_date = FakeDateTime()
        self.sun = Sun(latitude=TestSunShoud.FAKE_LATITUDE,
                       longitude=TestSunShoud.FAKE_LONGITUDE,
                       date=self.fake_date)

        self.fake_date_winter = FakeDateTime()
        self.fake_date_winter.set_winter()
        self.sun_winnter = Sun(latitude=TestSunShoud.FAKE_LATITUDE,
                               longitude=TestSunShoud.FAKE_LONGITUDE,
                               date=self.fake_date_winter)

    @classmethod
    def teardown_method(self, method):
        self.mock_requests_get = self.patcher_requests_get.stop()

    # ##############################################################################################
    def test__get_sunset__call_the_api_with_correct_data_and_location(self):
        self.sun.get_sunset()

        self.mock_requests_get.assert_called_once_with(url="{}/json?lat={}&lng={}&date={}".format(
            Sun.URL,
            TestSunShoud.FAKE_LATITUDE,
            TestSunShoud.FAKE_LONGITUDE,
            "{}-{}-{}".format(TestSunShoud.fake_date.year,
                              TestSunShoud.fake_date.month,
                              TestSunShoud.fake_date.day)
        ))

    def test__get_sunset__returns_sunset_hour_in_24h_and_local_format_summer(self):
        sunset = self.sun.get_sunset()

        assert sunset == TestSunShoud.FAKE_SUNSET_SUMMER

    def test__get_sunset__returns_sunset_hour_in_24h_and_local_format_winter(self):
        sunset = self.sun_winnter.get_sunset()

        assert sunset == TestSunShoud.FAKE_SUNSET_WINTER



