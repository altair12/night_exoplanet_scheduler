from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import pytest

from mock import patch

from night_scheduler.framework.sun.sun import Sun


class TestSun(object):
    FAKE_LATITUDE = "00"
    FAKE_LONGITUDE = "11"
    FAKE_DATE = "YYYY-MM-DD"
    FAKE_SUNSET = "99:88:77 PM"
    FAKE_SUNRISE_SUNSERT_ORG_ANSWER = {
        "results": {
            "sunrise": "4:26:42 AM",
            "sunset": "99:88:77 PM",
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
        self.mock_requests_get.return_value = TestSun.FAKE_SUNRISE_SUNSERT_ORG_ANSWER

        self.sun = Sun(latitude=TestSun.FAKE_LATITUDE,
                       longitude=TestSun.FAKE_LONGITUDE,
                       date=TestSun.FAKE_DATE)

    @classmethod
    def teardown_method(self, method):
        self.mock_requests_get = self.patcher_requests_get.stop()

    # ##############################################################################################
    def test__get_sunset__no_params__calou_and_today_called(self):
        self.sun.get_sunset()

        self.mock_requests_get.assert_called_once_with(url="{}/json?lat={}&lng={}&date={}".format(
            Sun.URL,
            TestSun.FAKE_LATITUDE,
            TestSun.FAKE_LONGITUDE,
            TestSun.FAKE_DATE
        ))

    def test__get_sunset__no_params__retuns_sunset_hour(self):
        sunset = self.sun.get_sunset()

        assert sunset == TestSun.FAKE_SUNSET