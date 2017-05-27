import requests

ETD_URL = "http://var2.astro.cz/ETD/predictions.php?delka=1&submit=submit&sirka=42"
SUNSET_URL = "https://www.timeanddate.com/sun/@6356250"


class NightExoplanetScheduler(object):
    def get_night_list(self):
        result = self.request(ETD_URL)
        print result.text

    def get_sunset(self):
        result = self.request(SUNSET_URL)
        print result.text

    def request(self, url):
        print(url)
        result = requests.get(url)
        return result



night = NightExoplanetScheduler()
night.get_sunset()

import time
print(time.localtime())
if time.localtime().tm_isdst:
    print("estiu +2")
else:
    print("hivern +1")
