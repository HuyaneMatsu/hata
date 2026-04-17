__all__ = ('PollLayout',)

from ...bases import Preinstance as P, PreinstancedBase


class PollLayout(PreinstancedBase, value_type = int):
    """
    Represents a poll's layout.
    
    Attributes
    ----------
    name : `str`
        The name of the poll layout.
    
    value : `int`
        The identifier value the poll layout.
    
    Type Attributes
    ---------------
    Every predefined poll layout can be accessed as type attribute as well:
    
    +-----------------------+-------------------+-------+
    | Type attribute name   | Name              | Value |
    +=======================+===================+=======+
    | none                  | none              | 0     |
    +-----------------------+-------------------+-------+
    | default               | default           | 1     |
    +-----------------------+-------------------+-------+
    """
    __slots__ = ()
    
    none = P(0, 'none')
    default = P(1, 'default')
