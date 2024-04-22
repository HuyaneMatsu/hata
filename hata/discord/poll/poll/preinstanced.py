__all__ = ('PollLayout',)

from ...bases import Preinstance as P, PreinstancedBase


class PollLayout(PreinstancedBase):
    """
    Represents a poll's layout.
    
    Attributes
    ----------
    name : `str`
        The name of the poll layout.
    value : `int`
        The identifier value the poll layout.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``PollLayout``) items
        Stores the predefined ``PollLayout``-s. These can be accessed with their `value` as key.
    VALUE_TYPE : `type` = `int`
        The poll layouts' values' type.
    DEFAULT_NAME : `str` = `'UNDEFINED'`
        The default name of the poll layouts.
    
    Every predefined poll layout can be accessed as class attribute as well:
    
    +-----------------------+-------------------+-------+
    | Class attribute name  | Name              | Value |
    +=======================+===================+=======+
    | none                  | none              | 0     |
    +-----------------------+-------------------+-------+
    | default               | default           | 1     |
    +-----------------------+-------------------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    DEFAULT_NAME = 'UNDEFINED'
    
    __slots__ = ()
    
    none = P(0, 'none')
    default = P(1, 'default')
