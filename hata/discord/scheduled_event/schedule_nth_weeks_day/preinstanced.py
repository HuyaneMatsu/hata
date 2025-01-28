__all__ = ('ScheduleWeeksDay',)

from ...bases import Preinstance as P, PreinstancedBase


class ScheduleWeeksDay(PreinstancedBase, value_type = int):
    """
    Represents a day of a week.
    
    Attributes
    ----------
    name : `str`
        The name of the schedule week's day.
    
    value : `int`
        The unique identifier of the schedule week's day.
    
    Type Attributes
    ---------------
    Each schedule week day is stored as a type attribute:
    
    +-----------------------+-----------+-----------------------+
    | Class Attribute name  | value     | name                  |
    +=======================+===========+=======================+
    | monday                | 0         | monday                |
    +-----------------------+-----------+-----------------------+
    | tuesday               | 1         | tuesday               |
    +-----------------------+-----------+-----------------------+
    | wednesday             | 2         | wednesday             |
    +-----------------------+-----------+-----------------------+
    | thursday              | 3         | thursday              |
    +-----------------------+-----------+-----------------------+
    | friday                | 4         | friday                |
    +-----------------------+-----------+-----------------------+
    | saturday              | 5         | saturday              |
    +-----------------------+-----------+-----------------------+
    | sunday                | 6         | sunday                |
    +-----------------------+-----------+-----------------------+
    """
    __slots__ = ()
    
    monday = P(0, 'monday')
    tuesday = P(1, 'tuesday')
    wednesday = P(2, 'wednesday')
    thursday = P(3, 'thursday',)
    friday = P(4, 'friday')
    saturday = P(5, 'saturday')
    sunday = P(6, 'sunday')
