"""Date with a specific timezone
Examples:
    date_time.date_time(2018, 12, 6, 8, 54, 32, format_=fmt)
    date_time.time(manipulate=True, manipulation_type='SUB', format_=fmt,
                    hours=1)
    date_time.time()
"""

from os import getenv
from datetime import datetime, timedelta
import pytz
from pytz import timezone

fmt = '%Y-%m-%d %H:%M:%S %Z%z'

tz = getenv('TIMEZONE', 'Africa/Lagos')


class DateTime(object):
    """Generates datetime according to the timezone."""
    def __init__(self, time_zone=None):
        self.UTC = pytz.utc
        self.time_zone = timezone(time_zone) if time_zone else self.UTC

    def date_time(self, *arg, format_=None):
        """Process a specified Date time.
        Args:
            *arg: The date to be parse
                year (int): The Year
                month (int): The Month
                day (int): The day
                minute (int): The minute
                second (int): The Seconds
            format_:
        Returns:
            Datetime: Formatted output
        """
        year, month, day, hour, minute, second = arg
        utc_dt = datetime(year,
                          month,
                          day,
                          hour,
                          minute,
                          second,
                          tzinfo=self.UTC)
        loc_dt = utc_dt.astimezone(self.time_zone)
        return self._output(loc_dt, format_)

    def _now(self):
        """Generate the current datetime.
        Returns:
            Datetime: The date time.
        """
        now = datetime.now()
        local_dt = now.astimezone(self.time_zone)
        return local_dt

    def _date_manipulation(self, now, type_='ADD', **kwargs):
        """Performs all date time manipulations on the provided datetime.
        Args:
            now (func): The date time to add to it.
            type_ (str): Type of manipulation
            **kwargs:
                minutes
                hours
                seconds
                milliseconds
        Returns:
            Datetime: The resulting date time.
        """
        dt = now()

        type_mapper = {
            'ADD': dt + timedelta(**kwargs),
            'SUB': dt - timedelta(**kwargs),
        }

        exists = type_mapper.get(type_)
        new_time = type_mapper[type_] if exists else type_mapper['ADD']
        local_dt_norm = self.time_zone.normalize(new_time)
        return local_dt_norm

    def _output(self, local_dt, format_=None):
        """Outputs the date time.
        Args:
            local_dt (datetime): The local datetime
            format_ (str): Strftime Format string
        Returns:
            Datetime: Formatted date time.
        """
        return local_dt.strftime(format_) if format_ else local_dt

    def time(self,
             manipulate=False,
             manipulation_type='ADD',
             format_=None,
             **kwargs):
        """Returns the datetime.
        Args:
            manipulate (bool): Toggles the date manipulation
            manipulation_type (str): The manipulation type
            format_ (str): Strtftime format string
            **kwargs (unknown): Arguments for timedelta
                minutes
                hours
                seconds
                milliseconds
        Returns:
            Datetime: The resulting datetime
        """

        mapper = {
            'NOW':
            self._output(self._now(), format_),
            'MANIPULATE':
            self._output(
                self._date_manipulation(self._now,
                                        type_=manipulation_type,
                                        **kwargs), format_)
        }

        return mapper['MANIPULATE'] if manipulate else mapper['NOW']


date_time = DateTime(tz)
