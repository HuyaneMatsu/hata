__all__ = ('ReactionType',)

from ...bases import Preinstance as P, PreinstancedBase


class ReactionType(PreinstancedBase):
    """
    Represents a reaction's type.
    
    Attributes
    ----------
    name : `str`
        The default name of the reaction type.
    value : `int`
        The discord side identifier value of the reaction type.    Class Attributes
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``ReactionType``) items
        Stores the predefined ``ReactionType``-s. These can be accessed with their `value` as key.
    VALUE_TYPE : `type` = `int`
        The reaction type' values' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the reaction type.
    
    Every predefined reaction type can be accessed as class attribute as well:
    
    +-----------------------+---------------+-------+
    | Class attribute name  | name          | value |
    +======================+================+=======+
    | standard              | standard      | 0     |
    +-----------------------+---------------+-------+
    | burst                 | status        | 1     |
    +-----------------------+---------------+-------+
    """
    __slots__ = ()
    
    INSTANCES = {}
    VALUE_TYPE = int
    
    standard = P(0, 'standard')
    burst = P(1, 'burst')
