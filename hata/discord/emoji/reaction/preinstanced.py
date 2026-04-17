__all__ = ('ReactionType',)

from ...bases import Preinstance as P, PreinstancedBase


class ReactionType(PreinstancedBase, value_type = int):
    """
    Represents a reaction's type.
    
    Attributes
    ----------
    name : `str`
        The default name of the reaction type.
    
    value : `int`
        The discord side identifier value of the reaction type.
    
    Type Attributes
    ---------------
    Every predefined reaction type can be accessed as type attribute as well:
    
    +-----------------------+---------------+-------+
    | Type attribute name   | name          | value |
    +======================+================+=======+
    | standard              | standard      | 0     |
    +-----------------------+---------------+-------+
    | burst                 | status        | 1     |
    +-----------------------+---------------+-------+
    """
    __slots__ = ()
    
    standard = P(0, 'standard')
    burst = P(1, 'burst')
