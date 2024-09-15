import jdatetime
from unidecode import unidecode


def jalali_to_gregorian(date):
    date = unidecode(f"{date}")
    date = date.split("/")
    date = jdatetime.date(int(date[0]), int(date[1]), int(date[2]), locale="fa_IR")
    date = jdatetime.date.togregorian(date)
    return date