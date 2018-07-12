from datetime import datetime, timedelta
from pytz import timezone
from datetime import tzinfo


ZERO = timedelta(0)
HOUR = timedelta(hours=1)
DSTSTART = datetime(1, 4, 1, 2)
DSTEND = datetime(1, 10, 25, 1)


class UTC(tzinfo):
    """UTC"""

    def utcoffset(self, dt):
        return ZERO

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return ZERO

def first_sunday_on_or_after(dt):
    days_to_go = 6 - dt.weekday()
    if days_to_go:
        dt += timedelta(days_to_go)
    return dt

class USTimeZone(tzinfo):

    def __init__(self, hours, reprname, stdname, dstname):
        self.stdoffset = timedelta(hours=hours)
        self.reprname = reprname
        self.stdname = stdname
        self.dstname = dstname

    def __repr__(self):
        return self.reprname

    def tzname(self, dt):
        if self.dst(dt):
            return self.dstname
        else:
            return self.stdname

    def utcoffset(self, dt):
        return self.stdoffset + self.dst(dt)

    def dst(self, dt):
        if dt is None or dt.tzinfo is None:
            # An exception may be sensible here, in one or both cases.
            # It depends on how you want to treat them.  The default
            # fromutc() implementation (called by the default astimezone()
            # implementation) passes a datetime with dt.tzinfo is self.
            return ZERO
        assert dt.tzinfo is self

        # Find first Sunday in April & the last in October.
        start = first_sunday_on_or_after(DSTSTART.replace(year=dt.year))
        end = first_sunday_on_or_after(DSTEND.replace(year=dt.year))

        # Can't compare naive to aware objects, so strip the timezone from
        # dt first.
        if start <= dt.replace(tzinfo=None) < end:
            return HOUR
        else:
            return ZERO

Eastern  = USTimeZone(-5, "Eastern",  "EST", "EDT")
Central  = USTimeZone(-6, "Central",  "CST", "CDT")
Mountain = USTimeZone(-7, "Mountain", "MST", "MDT")
Pacific  = USTimeZone(-8, "Pacific",  "PST", "PDT")

utc = UTC()

curr_time = '15:00:00'
eastern = timezone('US/Eastern')
western = timezone('US/Pacific')


def convert_timezone(show_date, show_time):
    date_lst = show_date.split('-')
    time_str = show_time.strftime('%H:%M:%S')
    time_lst = time_str.split(':')
    local_dt = datetime(int(date_lst[0]), int(date_lst[1]), int(date_lst[2]), int(time_lst[0]), int(time_lst[1]), int(time_lst[2]), tzinfo=Pacific)
    utc_dt = local_dt.astimezone(utc)
    return utc_dt


