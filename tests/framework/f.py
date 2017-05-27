import datetime

date = datetime.datetime.now()

print date
print(date + datetime.timedelta(days=1))



class FAKEDateTime(object):
    year = 9999
    month = 1
    day = 1



FAKE_DATE = FAKEDateTime
print("{}-{}-{}".format(FAKE_DATE.year, FAKE_DATE.month, FAKE_DATE.day))