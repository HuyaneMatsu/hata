__all__ = ('ScheduleFrequency', 'ScheduleMonth', )

from ...bases import Preinstance as P, PreinstancedBase


class ScheduleFrequency(PreinstancedBase, value_type = int):
    """
    Represents how often a scheduled event occurs.
    
    Attributes
    ----------
    name : `str`
        The name of the schedule frequency.
    
    value : `int`
        The unique identifier of the schedule frequency.
    
    Type Attributes
    ---------------
    Each schedule frequency is stored as a type attribute:
    
    +-----------------------+-----------+-----------------------+
    | Class Attribute name  | value     | name                  |
    +=======================+===========+=======================+
    | yearly                | 0         | yearly                |
    +-----------------------+-----------+-----------------------+
    | monthly               | 1         | monthly               |
    +-----------------------+-----------+-----------------------+
    | weekly                | 2         | weekly                |
    +-----------------------+-----------+-----------------------+
    | daily                 | 3         | daily                 |
    +-----------------------+-----------+-----------------------+
    """
    __slots__ = ()
    
    yearly = P(0, 'yearly')
    monthly = P(1, 'monthly')
    weekly = P(2, 'weekly')
    daily = P(3, 'daily')


class ScheduleMonth(PreinstancedBase, value_type = int):
    """
    Represents a day of a week.
    
    Attributes
    ----------
    name : `str`
        The name of the schedule month.
    
    value : `int`
        The unique identifier of the schedule month.
    
    Type Attributes
    ---------------
    Each schedule month is stored as a type attribute:
    
    +-----------------------+-----------+-----------------------+
    | Class Attribute name  | value     | name                  |
    +=======================+===========+=======================+
    | january               | 1         | january               |
    +-----------------------+-----------+-----------------------+
    | february              | 2         | february              |
    +-----------------------+-----------+-----------------------+
    | march                 | 3         | march                 |
    +-----------------------+-----------+-----------------------+
    | april                 | 4         | april                 |
    +-----------------------+-----------+-----------------------+
    | may                   | 5         | may                   |
    +-----------------------+-----------+-----------------------+
    | june                  | 6         | june                  |
    +-----------------------+-----------+-----------------------+
    | july                  | 7         | july                  |
    +-----------------------+-----------+-----------------------+
    | august                | 8         | august                |
    +-----------------------+-----------+-----------------------+
    | september             | 9         | september             |
    +-----------------------+-----------+-----------------------+
    | october               | 10        | october               |
    +-----------------------+-----------+-----------------------+
    | november              | 11        | november              |
    +-----------------------+-----------+-----------------------+
    | december              | 12        | december              |
    +-----------------------+-----------+-----------------------+
    """
    __slots__ = ()
    
    january = P(1, 'january')
    february = P(2, 'february')
    march = P(3, 'march')
    april = P(4, 'april',)
    may = P(5, 'may')
    june = P(6, 'june')
    july = P(7, 'july')
    august = P(8, 'august')
    september = P(9, 'september')
    october = P(10, 'october')
    november = P(11, 'november')
    december = P(12, 'december')


# Set january as default, lets not talk about it...
ScheduleMonth.INSTANCES[0] = ScheduleMonth.january
