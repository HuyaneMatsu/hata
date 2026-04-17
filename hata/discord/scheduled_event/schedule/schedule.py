__all__ = ('Schedule',)

from datetime import datetime as DateTime

from scarletio import RichAttributeErrorBaseType

from ...utils import DATETIME_FORMAT_CODE, DISCORD_EPOCH_START

from ..schedule_nth_weeks_day import ScheduleNthWeeksDay, ScheduleWeeksDay

from .fields import (
    parse_by_month_days, parse_by_months, parse_by_nth_weeks_days, parse_by_weeks_days, parse_by_year_days, parse_end,
    parse_frequency, parse_occurrence_count_limit, parse_occurrence_spacing, parse_start, put_by_month_days,
    put_by_months, put_by_nth_weeks_days, put_by_weeks_days, put_by_year_days, put_end,
    put_frequency, put_occurrence_count_limit, put_occurrence_spacing, put_start,
    validate_by_month_days, validate_by_months, validate_by_nth_weeks_days, validate_by_weeks_days,
    validate_by_year_days, validate_end, validate_frequency, validate_occurrence_count_limit,
    validate_occurrence_spacing, validate_start
)
from .preinstanced import ScheduleFrequency, ScheduleMonth


class Schedule(RichAttributeErrorBaseType):
    """
    The schedule of a scheduled event.
    
    There are many limitation and many fields are also mutually exclusive.
    These are not checked directly here, so you will have tinker how things work by yourself.
    If you do not want to tinker, there are presents you may want to try out:
    - ``.create_weekly`` (example: every day )
    - ``.create_weekly`` (example: every sunday we go shopping)
    - ``.create_bi_weekly`` (example: every second saturday we visit people)
    - ``.create_monthly_nth_weeks_day`` (example: every month 1st week sunday we play chicken horse)
    - ``.create_yearly_month_nth_day`` (example: every year january 13 is someone's birthday)
    
    More may be added as required.
    
    Attributes
    ----------
    by_month_days : `None | tuple<int>`
        On which days of the month should the event occur at.
    
    by_months : `None | tuple<ScheduleMonth>`
        On which months should the event occur at.
    
    by_nth_weeks_days : `None | tuple<ScheduleNthWeeksDay>`
        On which days the event should occur at.
    
    by_weeks_days : `None | tuple<ScheduleWeeksDay>`
        In which days of the week should the event occur at.
    
    by_year_days : `None | tuple<int>`
        On which days of the year should the even occur at.
    
    end : `None | DateTime`
        When the occurrence should end at.
    
    frequency : ``ScheduleFrequency``
        How often should the event occur.
    
    occurrence_count_limit : `int`
        Up to how much times should the event occur.
    
    occurrence_spacing : `int`
        The spacing between 2 events.
        If set as `1` means it should occur on every occasion.
        If set to `2` it will occur only on every other.
    
    start : `None | DateTime`
        When the occurrence should start at.
    """
    __slots__ = (
        'by_month_days', 'by_months', 'by_nth_weeks_days', 'by_weeks_days', 'by_year_days', 'end', 'frequency',
        'occurrence_count_limit', 'occurrence_spacing', 'start'
    )
    
    def __new__(
        cls,
        by_month_days = ...,
        by_months = ...,
        by_nth_weeks_days = ...,
        by_weeks_days = ...,
        by_year_days = ...,
        end = ...,
        frequency = ...,
        occurrence_count_limit = ...,
        occurrence_spacing = ...,
        start = ...,
    ):
        """
        Creates a schedule with the given fields.
        
        Parameters
        ----------
        by_month_days : `None | iterable<int>`, Optional (Keyword only)
            On which days of the month should the event occur at.
        
        by_months : `None | iterable<ScheduleMonth> | iterable<int>`, Optional (Keyword only)
            On which months should the event occur at.
        
        by_nth_weeks_days : `None | iterable<ScheduleNthWeeksDay>`, Optional (Keyword only)
            On which days the event should occur at.
        
        by_weeks_days : `None | iterable<ScheduleWeeksDay> | iterable<int>`, Optional (Keyword only)
            In which days of the week should the event occur at.
        
        by_year_days : `None | iterable<int>`, Optional (Keyword only)
            On which days of the year should the even occur at.
        
        end : `None | DateTime`, Optional (Keyword only)
            When the occurrence should end at.
        
        frequency : `ScheduleFrequency | int`, Optional (Keyword only)
            How often should the event occur.
        
        occurrence_count_limit : `int`, Optional (Keyword only)
            Up to how much times should the event occur.
        
        occurrence_spacing : `int`, Optional (Keyword only)
            The spacing between 2 events.
        
        start : `None | DateTime`, Optional (Keyword only)
            When the occurrence should start at.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # by_month_days
        if by_month_days is ...:
            by_month_days = None
        else:
            by_month_days = validate_by_month_days(by_month_days)
        
        # by_months
        if by_months is ...:
            by_months = None
        else:
            by_months = validate_by_months(by_months)
        
        # by_nth_weeks_days
        if by_nth_weeks_days is ...:
            by_nth_weeks_days = None
        else:
            by_nth_weeks_days = validate_by_nth_weeks_days(by_nth_weeks_days)
        
        # by_weeks_days
        if by_weeks_days is ...:
            by_weeks_days = None
        else:
            by_weeks_days = validate_by_weeks_days(by_weeks_days)
        
        # by_year_days
        if by_year_days is ...:
            by_year_days = None
        else:
            by_year_days = validate_by_year_days(by_year_days)
        
        # end
        if end is ...:
            end = None
        else:
            end = validate_end(end)
        
        # frequency
        if frequency is ...:
            frequency = ScheduleFrequency.yearly
        else:
            frequency = validate_frequency(frequency)
        
        # occurrence_count_limit
        if occurrence_count_limit is ...:
            occurrence_count_limit = 0
        else:
            occurrence_count_limit = validate_occurrence_count_limit(occurrence_count_limit)
        
        # occurrence_spacing
        if occurrence_spacing is ...:
            occurrence_spacing = 1
        else:
            occurrence_spacing = validate_occurrence_spacing(occurrence_spacing)
        
        # start
        if start is ...:
            start = None
        else:
            start = validate_start(start)
        
        # construct
        self = object.__new__(cls)
        self.by_month_days = by_month_days
        self.by_months = by_months
        self.by_nth_weeks_days = by_nth_weeks_days
        self.by_weeks_days = by_weeks_days
        self.by_year_days = by_year_days
        self.end = end
        self.frequency = frequency
        self.occurrence_count_limit = occurrence_count_limit
        self.occurrence_spacing = occurrence_spacing
        self.start = start
        return self
    
    
    def __repr__(self):
        """Returns the representation of the schedule."""
        repr_parts = ['<', type(self).__name__]
        
        # frequency
        frequency = self.frequency
        repr_parts.append(' frequency = ')
        repr_parts.append(frequency.name)
        
        # yearlies
        if frequency is ScheduleFrequency.yearly:
            # by_year_days
            by_year_days = self.by_year_days
            if (by_year_days is not None):
                repr_parts.append(', by_year_days = ')
                repr_parts.append(repr(by_year_days))
            
            # by_months
            by_months = self.by_months
            if (by_months is not None):
                repr_parts.append(', by_months = ')
                repr_parts.append(repr(by_months))
        
        # yearlies and monthlies
        if frequency is ScheduleFrequency.yearly or ScheduleFrequency.monthly:
            # by_month_days
            by_month_days = self.by_month_days
            if (by_month_days is not None):
                repr_parts.append(', by_month_days = ')
                repr_parts.append(repr(by_month_days))
            
            # by_nth_weeks_days
            by_nth_weeks_days = self.by_nth_weeks_days
            if (by_nth_weeks_days is not None):
                repr_parts.append(', by_nth_weeks_days = ')
                repr_parts.append(repr(by_nth_weeks_days))
        
        # weeklies and dailies
        if frequency is ScheduleFrequency.weekly or frequency is ScheduleFrequency.daily:
            by_weeks_days = self.by_weeks_days
            if (by_weeks_days is not None):
                repr_parts.append(', by_weeks_days = ')
                repr_parts.append(repr(by_weeks_days))
        
        # occurrence_spacing
        occurrence_spacing = self.occurrence_spacing
        if (occurrence_spacing != 1):
            repr_parts.append(', occurrence_spacing = ')
            repr_parts.append(repr(occurrence_spacing))
        
        # occurrence_count_limit
        occurrence_count_limit = self.occurrence_count_limit
        if (occurrence_count_limit != 0):
            repr_parts.append(', occurrence_count_limit = ')
            repr_parts.append(repr(occurrence_count_limit))
        
        # start
        start = self.start
        if (start is not None):
            repr_parts.append(', start = ')
            repr_parts.append(format(start, DATETIME_FORMAT_CODE))
        
        # end
        end = self.end
        if (end is not None):
            repr_parts.append(', end = ')
            repr_parts.append(format(end, DATETIME_FORMAT_CODE))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two schedules are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.by_month_days != other.by_month_days:
            return False
        
        if self.by_months != other.by_months:
            return False
        
        if self.by_nth_weeks_days != other.by_nth_weeks_days:
            return False
        
        if self.by_weeks_days != other.by_weeks_days:
            return False
        
        if self.by_year_days != other.by_year_days:
            return False
        
        if self.end != other.end:
            return False
        
        if self.frequency is not other.frequency:
            return False
        
        if self.occurrence_count_limit != other.occurrence_count_limit:
            return False
        
        if self.occurrence_spacing != other.occurrence_spacing:
            return False
        
        if self.start != other.start:
            return False
        
        return True
    
    
    def __hash__(self):
        """Returns the schedule's hash value."""
        hash_value = 0
        
        # by_month_days
        by_month_days = self.by_month_days
        if (by_month_days is not None):
            hash_value ^= len(by_month_days) << 0
            
            for by_month_day in by_month_days:
                hash_value ^= hash(by_month_day) << 1
        
        # by_months
        by_months = self.by_months
        if (by_months is not None):
            hash_value ^= len(by_months) << 2
            
            for by_month in by_months:
                hash_value ^= hash(by_month) << 3

        # by_nth_weeks_days
        by_nth_weeks_days = self.by_nth_weeks_days
        if (by_nth_weeks_days is not None):
            hash_value ^= len(by_nth_weeks_days) << 4
            
            for by_nth_weeks_day in by_nth_weeks_days:
                hash_value ^= hash(by_nth_weeks_day) << 5

        # by_weeks_days
        by_weeks_days = self.by_weeks_days
        if (by_weeks_days is not None):
            hash_value ^= len(by_weeks_days) << 6
            
            for by_weeks_day in by_weeks_days:
                hash_value ^= hash(by_weeks_day) << 7

        # by_year_days
        by_year_days = self.by_year_days
        if (by_year_days is not None):
            hash_value ^= len(by_year_days) << 8
            
            for by_year_day in by_year_days:
                hash_value ^= hash(by_year_day) << 9
        
        # end
        end = self.end
        if (end is not None):
            hash_value ^= hash(end)
        
        # frequency
        hash_value ^= hash(self.frequency) << 10
        
        # occurrence_count_limit
        hash_value ^= self.occurrence_count_limit << 11
        
        # occurrence_spacing
        hash_value ^= self.occurrence_spacing << 12
        
        # start
        start = self.start
        if (start is not None):
            hash_value ^= hash(start)
        
        return hash_value
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a schedule from the given data.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Received data.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.by_month_days = parse_by_month_days(data)
        self.by_months = parse_by_months(data)
        self.by_nth_weeks_days = parse_by_nth_weeks_days(data)
        self.by_weeks_days = parse_by_weeks_days(data)
        self.by_year_days = parse_by_year_days(data)
        self.end = parse_end(data)
        self.frequency = parse_frequency(data)
        self.occurrence_count_limit = parse_occurrence_count_limit(data)
        self.occurrence_spacing = parse_occurrence_spacing(data)
        self.start = parse_start(data)
        return self
    
    
    def to_data(self, *, defaults = False, start = None):
        """
        Converts the schedule to a json serializable object.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default values should be included as well.
        start : `None | DateTime` = `None`, Optional (Keyword only)
            Start date to use if schedule does not define it.
        
        Returns
        -------
        data : `dict<str, object>`
        """
        data = {}
        put_by_month_days(self.by_month_days, data, defaults)
        put_by_months(self.by_months, data, defaults)
        put_by_nth_weeks_days(self.by_nth_weeks_days, data, defaults)
        put_by_weeks_days(self.by_weeks_days, data, defaults)
        put_by_year_days(self.by_year_days, data, defaults)
        put_end(self.end, data, defaults)
        put_frequency(self.frequency, data, defaults)
        put_occurrence_count_limit(self.occurrence_count_limit, data, defaults)
        put_occurrence_spacing(self.occurrence_spacing, data, defaults)
        
        schedule_start = self.start
        if (schedule_start is None):
            if start is None:
                schedule_start = DISCORD_EPOCH_START
            else:
                schedule_start = start
        
        put_start(schedule_start, data, defaults)
        
        return data
    
    
    def copy(self):
        """
        Copies the schedule.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        
        # by_month_days
        by_month_days = self.by_month_days
        if (by_month_days is not None):
            by_month_days = (*by_month_days,)
        new.by_month_days = by_month_days
        
        # by_months
        by_months = self.by_months
        if (by_months is not None):
            by_months = (*by_months,)
        new.by_months = by_months
        
        # by_nth_weeks_days
        by_nth_weeks_days = self.by_nth_weeks_days
        if (by_nth_weeks_days is not None):
            by_nth_weeks_days = (*by_nth_weeks_days,)
        new.by_nth_weeks_days = by_nth_weeks_days
        
        # by_weeks_days
        by_weeks_days = self.by_weeks_days
        if (by_weeks_days is not None):
            by_weeks_days = (*by_weeks_days,)
        new.by_weeks_days = by_weeks_days
        
        # by_year_days
        by_year_days = self.by_year_days
        if (by_year_days is not None):
            by_year_days = (*by_year_days,)
        new.by_year_days = by_year_days
        
        new.end = self.end
        new.frequency = self.frequency
        new.occurrence_count_limit = self.occurrence_count_limit
        new.occurrence_spacing = self.occurrence_spacing
        new.start = self.start
        
        return new
    
    
    def copy_with(
        self,
        by_month_days = ...,
        by_months = ...,
        by_nth_weeks_days = ...,
        by_weeks_days = ...,
        by_year_days = ...,
        end = ...,
        frequency = ...,
        occurrence_count_limit = ...,
        occurrence_spacing = ...,
        start = ...,
    ):
        """
        Copies the schedule with the given fields.
        
        Parameters
        ----------
        by_month_days : `None | iterable<int>`, Optional (Keyword only)
            On which days of the month should the event occur at.
        
        by_months : `None | iterable<ScheduleMonth> | iterable<int>`, Optional (Keyword only)
            On which months should the event occur at.
        
        by_nth_weeks_days : `None | iterable<ScheduleNthWeeksDay>`, Optional (Keyword only)
            On which days the event should occur at.
        
        by_weeks_days : `None | iterable<ScheduleWeeksDay> | iterable<int>`, Optional (Keyword only)
            In which days of the week should the event occur at.
        
        by_year_days : `None | iterable<int>`, Optional (Keyword only)
            On which days of the year should the even occur at.
        
        end : `None | DateTime`, Optional (Keyword only)
            When the occurrence should end at.
        
        frequency : `ScheduleFrequency | int`, Optional (Keyword only)
            How often should the event occur.
        
        occurrence_count_limit : `int`, Optional (Keyword only)
            Up to how much times should the event occur.
        
        occurrence_spacing : `int`, Optional (Keyword only)
            The spacing between 2 events.
        
        start : `None | DateTime`, Optional (Keyword only)
            When the occurrence should start at.
        
        Returns
        -------
        new : `instance<type<self>>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # by_month_days
        if by_month_days is ...:
            by_month_days = self.by_month_days
            if (by_month_days is not None):
                by_month_days = (*by_month_days,)
        else:
            by_month_days = validate_by_month_days(by_month_days)
        
        # by_months
        if by_months is ...:
            by_months = self.by_months
            if (by_months is not None):
                by_months = (*by_months,)
        else:
            by_months = validate_by_months(by_months)
        
        # by_nth_weeks_days
        if by_nth_weeks_days is ...:
            by_nth_weeks_days = self.by_nth_weeks_days
            if (by_nth_weeks_days is not None):
                by_nth_weeks_days = (*by_nth_weeks_days,)
        else:
            by_nth_weeks_days = validate_by_nth_weeks_days(by_nth_weeks_days)
        
        # by_weeks_days
        if by_weeks_days is ...:
            by_weeks_days = self.by_weeks_days
            if (by_weeks_days is not None):
                by_weeks_days = (*by_weeks_days,)
        else:
            by_weeks_days = validate_by_weeks_days(by_weeks_days)
        
        # by_year_days
        if by_year_days is ...:
            by_year_days = self.by_year_days
            if (by_year_days is not None):
                by_year_days = (*by_year_days,)
        else:
            by_year_days = validate_by_year_days(by_year_days)
        
        # end
        if end is ...:
            end = self.end
        else:
            end = validate_end(end)
        
        # frequency
        if frequency is ...:
            frequency = self.frequency
        else:
            frequency = validate_frequency(frequency)
        
        # occurrence_count_limit
        if occurrence_count_limit is ...:
            occurrence_count_limit = self.occurrence_count_limit
        else:
            occurrence_count_limit = validate_occurrence_count_limit(occurrence_count_limit)
        
        # occurrence_spacing
        if occurrence_spacing is ...:
            occurrence_spacing = self.occurrence_spacing
        else:
            occurrence_spacing = validate_occurrence_spacing(occurrence_spacing)
        
        # start
        if start is ...:
            start = self.start
        else:
            start = validate_start(start)
        
        # construct
        new = object.__new__(type(self))
        new.by_month_days = by_month_days
        new.by_months = by_months
        new.by_nth_weeks_days = by_nth_weeks_days
        new.by_weeks_days = by_weeks_days
        new.by_year_days = by_year_days
        new.end = end
        new.frequency = frequency
        new.occurrence_count_limit = occurrence_count_limit
        new.occurrence_spacing = occurrence_spacing
        new.start = start
        return new
    
    
    @classmethod
    def create_weekly(cls, day):
        """
        Creates a new schedule that occurs weekly on a specific day.
        
        Parameters
        ----------
        day : ``ScheduleWeeksDay``
            The day to occur at.
        
        Returns
        -------
        self : `instance<cls>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        return cls(
            by_weeks_days = [day],
            frequency = ScheduleFrequency.weekly,
        )

    
    @classmethod
    def create_bi_weekly(cls, day):
        """
        Creates a new schedule that occurs every other week on a specific day.
        
        Parameters
        ----------
        day : ``ScheduleWeeksDay``
            The day to occur at.
        
        Returns
        -------
        self : `instance<cls>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        return cls(
            by_weeks_days = [day],
            frequency = ScheduleFrequency.weekly,
            occurrence_spacing = 2,
        )
    
    
    @classmethod
    def create_monthly_nth_weeks_day(cls, nth_week, weeks_day):
        """
        Creates a new schedule that occurs every month on the nth week's same day.
        
        Parameters
        ----------
        nth_week : `int`
            The nth week to re-occur at.
        weeks_day : ``ScheduleWeeksDay``
            The day of the week.
        
        Returns
        -------
        self : `instance<cls>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        return cls(
            by_nth_weeks_days = [ScheduleNthWeeksDay(nth_week = nth_week, weeks_day = weeks_day)],
            frequency = ScheduleFrequency.monthly,
        )
    
    
    @classmethod
    def create_yearly_month_nth_day(cls, month, nth_day):
        """
        Creates a new schedule that occurs every year on the same month's nth day.
        
        Parameters
        ----------
        month : ``ScheduleMonth``
            The month of the year to re-occur at.
        nth_day : `int`
            The nth day of the month.
        
        Returns
        -------
        self : `instance<cls>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        return cls(
            by_month_days = [nth_day],
            by_months = [month],
            frequency = ScheduleFrequency.yearly,
        )
