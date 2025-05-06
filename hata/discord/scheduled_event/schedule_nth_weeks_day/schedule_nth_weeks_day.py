__all__ = ('ScheduleNthWeeksDay',)

from scarletio import RichAttributeErrorBaseType

from .fields import (
    parse_nth_week, parse_weeks_day, put_nth_week, put_weeks_day, validate_nth_week, validate_weeks_day
)
from .preinstanced import ScheduleWeeksDay


class ScheduleNthWeeksDay(RichAttributeErrorBaseType):
    """
    Represents a day of the nth week of a month.
    
    Attributes
    ----------
    nth_week : `int`
        The week of the month.
    weeks_day : ``ScheduleWeeksDay``
        The day of the week.
    """
    __slots__ = ('nth_week', 'weeks_day')
    
    def __new__(cls, *, nth_week = ..., weeks_day = ...):
        """
        Creates a new nth week's day.
        
        Parameters
        ----------
        nth_week : `int`, Optional (Keyword only)
            The week of the month.
        weeks_day : ``ScheduleWeeksDay``, `int`, Optional (Keyword only)
            The day of the week.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # nth_week
        if nth_week is ...:
            nth_week = 1
        else:
            nth_week = validate_nth_week(nth_week)
        
        # weeks_day
        if weeks_day is ...:
            weeks_day = ScheduleWeeksDay.monday
        else:
            weeks_day = validate_weeks_day(weeks_day)
        
        # construct
        self = object.__new__(cls)
        self.nth_week = nth_week
        self.weeks_day = weeks_day
        return self
    
    
    def __repr__(self):
        """Returns the nth week's day's representation."""
        repr_parts = ['<', type(self).__name__]
        
        # nth_week
        repr_parts.append(' nth_week = ')
        repr_parts.append(repr(self.nth_week))
        
        # weeks_day
        repr_parts.append(' weeks_day = ')
        repr_parts.append(self.weeks_day.name)
        # Skip adding " ~ value"
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two nth week's days are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        # nth_week
        if self.nth_week != other.nth_week:
            return False
        
        # weeks_day
        if self.weeks_day is not other.weeks_day:
            return False
        
        return True
    
    
    def __gt__(self, other):
        """Returns whether the two nth week's days is greater than the other."""
        if type(self) is not type(other):
            return NotImplemented
        
        # nth_week
        self_nth_week = self.nth_week
        other_nth_week = other.nth_week
        if self_nth_week > other_nth_week:
            return True
        
        if self_nth_week != other_nth_week:
            return False
        
        # weeks_day
        if self.weeks_day > other.weeks_day:
            return True
        
        return False
    
    
    def __hash__(self):
        """Returns whether the two nth week's days hash value."""
        hash_value = 0
        
        # nth_week
        hash_value ^= self.nth_week << 4
        
        # weeks_day
        hash_value ^= hash(self.weeks_day)
        
        return hash_value
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new nth week's day from the given data.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Data.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.nth_week = parse_nth_week(data)
        self.weeks_day = parse_weeks_day(data)
        return self
    
    
    def to_data(self, *, defaults = False):
        """
        Converts the schedule nth week's day to a serializable object.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default field values should be included.
        
        Returns
        -------
        data : `dict<str, object>`
        """
        data = {}
        put_nth_week(self.nth_week, data, defaults)
        put_weeks_day(self.weeks_day, data, defaults)
        return data
    
    
    def copy(self):
        """
        Returns a copy of the nth week's day.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.nth_week = self.nth_week
        new.weeks_day = self.weeks_day
        return new
    
    
    def copy_with(self, *, nth_week = ..., weeks_day = ...):
        """
        Returns the copy of the nth week's day with the given fields.
        
        Parameters
        ----------
        nth_week : `int`, Optional (Keyword only)
            The week of the month.
        weeks_day : ``ScheduleWeeksDay``, `int`, Optional (Keyword only)
            The day of the week.
        
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
        # nth_week
        if nth_week is ...:
            nth_week = self.nth_week
        else:
            nth_week = validate_nth_week(nth_week)
        
        # weeks_day
        if weeks_day is ...:
            weeks_day = self.weeks_day
        else:
            weeks_day = validate_weeks_day(weeks_day)
        
        # construct
        new = object.__new__(type(self))
        new.nth_week = nth_week
        new.weeks_day = weeks_day
        return new
