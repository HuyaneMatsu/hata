__all__ = ('ScheduleWeeksDay',)

from ...bases import Preinstance as P, PreinstancedBase


class ScheduleWeeksDay(PreinstancedBase):
    """
    Represents a day of a week.
    
    Attributes
    ----------
    value : `int`
        The unique identifier of the text decoration.
    name : `str`
        The default name of the text decoration.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`str`, ``ScheduleWeeksDay``) items
        The predefined schedule week days stored in `.value` - `object` relation.
    VALUE_TYPE : `type` = `int`
        Schedule week days' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name to use as the preinstanced objects'.
    
    Each schedule week day is stored as a class attribute:
    
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
    
    INSTANCES = {}
    VALUE_TYPE = int
    
    monday = P(0, 'monday')
    tuesday = P(1, 'tuesday')
    wednesday = P(2, 'wednesday')
    thursday = P(3, 'thursday',)
    friday = P(4, 'friday')
    saturday = P(5, 'saturday')
    sunday = P(6, 'sunday')
