__all__ = ('AutoModerationTriggerType',)

from ..bases import Preinstance as P, PreinstancedBase


class AutoModerationTriggerType(PreinstancedBase):
    """
    Represents an auto moderation rule's trigger.
    
    Attributes
    ----------
    value : `int`
        The Discord side identifier value of the auto moderation trigger type.
    name : `str`
        The default name of the auto moderation trigger type.
    max_per_guild : `int`
        The maximal amount of rules of this type per guild.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`str`, ``AutoModerationTriggerType``) items
        Stores the predefined auto moderation trigger types. This container is accessed when translating a Discord side
        identifier of a auto moderation trigger type. The identifier value is used as a key to get it's wrapper side
        representation.
    VALUE_TYPE : `type` = `str`
        The auto moderation trigger types' values' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the auto moderation trigger types.
    
    Every predefined auto moderation trigger type is also stored as a class attribute:
    
    +-----------------------+-------------------+-----------+---------------+
    | Class attribute name  | Name              | Value     | Max per guild |
    +=======================+===================+===========+===============+
    | none                  | none              | 0         | 0             |
    +-----------------------+-------------------+-----------+---------------+
    | keyword               | keyword           | 1         | 3             |
    +-----------------------+-------------------+-----------+---------------+
    | harmful_link          | harmful link      | 2         | 1             |
    +-----------------------+-------------------+-----------+---------------+
    | spam                  | spam              | 3         | 1             |
    +-----------------------+-------------------+-----------+---------------+
    | keyword_preset        | keyword preset    | 4         | 1             |
    +-----------------------+-------------------+-----------+---------------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    
    __slots__ = ('max_per_guild',)
    

    @classmethod
    def _from_value(cls, value):
        """
        Creates a new auto moderation trigger type with the given value.
        
        Parameters
        ----------
        value : `int`
            The auto moderation trigger type's identifier value.
        
        Returns
        -------
        self : ``AutoModerationTriggerType``
            The created instance.
        """
        self = object.__new__(cls)
        self.name = cls.DEFAULT_NAME
        self.value = value
        self.max_per_guild = value
        
        return self
    
    
    def __init__(self, value, name, max_per_guild):
        """
        Creates an ``AutoModerationTriggerType`` and stores it at the class's `.INSTANCES` class attribute as well.
        
        Parameters
        ----------
        value : `int`
            The Discord side identifier value of the auto moderation trigger type.
        name : `str`
            The default name of the auto moderation trigger type.
        max_per_guild : `int`
            The native name of the auto moderation trigger type.
        """
        self.value = value
        self.name = name
        self.max_per_guild = max_per_guild
        
        self.INSTANCES[value] = self
    
    # predefined
    none = P(0, 'none', 0)
    keyword = P(1, 'keyword', 3)
    harmful_link = P(2, 'harmful link', 1)
    spam = P(3, 'spam', 1)
    keyword_preset = P(4, 'keyword preset', 1)
