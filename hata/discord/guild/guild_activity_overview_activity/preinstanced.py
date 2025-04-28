__all__ = ('GuildActivityOverviewActivityLevel',)

from ...bases import Preinstance as P, PreinstancedBase


class GuildActivityOverviewActivityLevel(PreinstancedBase, value_type = int):
    """
    Represents a guild activity overview's activity's level.
    
    Attributes
    ----------
    name : `str`
        The name of the guild activity overview activity's level.
    
    value : `int`
        The identifier value the guild activity overview activity's level.
    
    Type Attributes
    ---------------
    Every predefined guild overview activity level can be accessed as type attribute as well:
    
    +-----------------------+-------------------+-------------------+
    | Type attribute name   | Name              | Value             |
    +=======================+===================+===================+
    | none                  | none              | 0                 |
    +-----------------------+-------------------+-------------------+
    | any_previous          | any previous      | 1                 |
    +-----------------------+-------------------+-------------------+
    | recently_popular      | recently popular  | 2                 |
    +-----------------------+-------------------+-------------------+
    """
    __slots__ = ()
    
    none = P(0, 'none')
    any_previous = P(1, 'any previous')
    recently_popular = P(2, 'recently popular')
