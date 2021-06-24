__all__ = ('StagePrivacyLevel', )

from ..bases import PreinstancedBase, Preinstance as P

class StagePrivacyLevel(PreinstancedBase):
    """
    Represents a stage channel's privacy level.
    
    Attributes
    ----------
    name : `str`
        The name of the stage privacy level.
    value : `int`
        The identifier value the stage privacy level.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``StagePrivacyLevel``) items
        Stores the predefined ``StagePrivacyLevel`` instances. These can be accessed with their `value` as key.
    VALUE_TYPE : `type` = `int`
        The stage privacy level' values' type.
    DEFAULT_NAME : `str` = `'UNDEFINED'`
        The default name of the stage privacy levels.
    
    Every predefined stage privacy level can be accessed as class attribute as well:
    
    +-----------------------+---------------+-------+
    | Class attribute name  | Name          | Value |
    +=======================+===============+=======+
    | none                  | none          | 0     |
    +-----------------------+---------------+-------+
    | public                | public        | 1     |
    +-----------------------+---------------+-------+
    | guild_only            | guild_only    | 2     |
    +-----------------------+---------------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    DEFAULT_NAME = 'UNDEFINED'
    
    __slots__ = ()
    
    none = P(0, 'none')
    public = P(1, 'public')
    guild_only = P(2, 'guild_only')
