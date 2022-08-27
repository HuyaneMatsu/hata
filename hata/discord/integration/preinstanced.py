__all__ = ('IntegrationExpireBehavior', 'IntegrationType')

from ..bases import Preinstance as P, PreinstancedBase


class IntegrationExpireBehavior(PreinstancedBase):
    """
    Represents an ``IntegrationDetail``'s expire behavior.
    
    Attributes
    ----------
    name : `str`
        The name of the integration expire behavior.
    value : `int`
        The Discord side identifier value of the integration expire behavior.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``IntegrationExpireBehavior``) items
        Stores the predefined ``IntegrationExpireBehavior``-s. These can be accessed with their `value` as key.
    VALUE_TYPE : `type` = `int`
        The integration expire behavior' values' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the integration expire behaviors.
    
    Every predefined expire behavior can be accessed as class attribute as well:
    
    +-----------------------+---------------+-------+
    | Class attribute name  | name          | value |
    +=======================+===============+=======+
    | remove_role           | remove_role   | 0     |
    +-----------------------+---------------+-------+
    | kick                  | kick          | 1     |
    +-----------------------+---------------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    
    __slots__ = ()
    
    # predefined
    remove_role = P(0, 'remove_role')
    kick = P(1, 'kick')



class IntegrationType(PreinstancedBase):
    """
    Represents an ``Integration``'s type.
    
    Attributes
    ----------
    name : `str`
        The name of the integration type.
    value : `int`
        The Discord side identifier value of the integration type.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`str`, ``IntegrationType``) items
        Stores the predefined ``IntegrationType``-s. These can be accessed with their `value` as key.
    VALUE_TYPE : `type` = `int`
        The integration type' values' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the integration types.
    
    Every predefined integration type can be accessed as class attribute as well:
    
    +-----------------------+---------------+---------------+
    | Class attribute name  | name          | value         |
    +=======================+===============+===============+
    | none                  | none          | `''`          |
    +-----------------------+---------------+---------------+
    | discord               | Discord       | `'discord'`   |
    +-----------------------+---------------+---------------+
    | youtube               | Youtube       | `'youtube'`   |
    +-----------------------+---------------+---------------+
    """
    INSTANCES = {}
    VALUE_TYPE = str
    
    __slots__ = ()
    

    @classmethod
    def _from_value(cls, value):
        """
        Creates a new integration type with the given value.
        
        Parameters
        ----------
        value : `str`
            The integration's type.
        
        Returns
        -------
        self : ``IntegrationType``
            The created instance.
        """
        self = object.__new__(cls)
        self.name = value
        self.value = value
        
        return self
    
    # predefined
    none = P('', 'none')
    discord = P('discord', 'Discord')
    youtube = P('youtube', 'Youtube')
