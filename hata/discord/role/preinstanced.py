__all__ = ('RoleManagerType',)

from ..bases import PreinstancedBase, Preinstance as P

class RoleManagerType(PreinstancedBase):
    """
    Represents a managed role's manager type.
    
    Attributes
    ----------
    name : `str`
        The name of the role manager type.
    value : `int`
        The identifier value the role manager type.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``RoleManagerType``) items
        Stores the predefined ``RoleManagerType`` instances. These can be accessed with their `value` as key.
    VALUE_TYPE : `type` = `int`
        The role manager types' values' type.
    DEFAULT_NAME : `str` = `'UNDEFINED'`
        The default name of the role manager types.
    
    Every predefined role manager type can be accessed as class attribute as well:
    
    +-----------------------+---------------+-------+
    | Class attribute name  | name          | value |
    +=======================+===============+=======+
    | none                  | none          | 0     |
    +-----------------------+---------------+-------+
    | unset                 | unset         | 1     |
    +-----------------------+---------------+-------+
    | unknown               | unknown       | 2     |
    +-----------------------+---------------+-------+
    | bot                   | bot           | 3     |
    +-----------------------+---------------+-------+
    | booster               | booster       | 4     |
    +-----------------------+---------------+-------+
    | integration           | integration   | 5     |
    +-----------------------+---------------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    DEFAULT_NAME = 'UNDEFINED'
    
    __slots__ = ()
    
    def __bool__(self):
        """Returns whether the role manager's type is set."""
        if self.value:
            boolean = True
        else:
            boolean = False
        
        return boolean
    
    none = P(0, 'none',)
    unset = P(1, 'unset',)
    unknown = P(2, 'unknown',)
    bot = P(3, 'bot',)
    booster = P(4, 'booster',)
    integration = P(5, 'integration',)
