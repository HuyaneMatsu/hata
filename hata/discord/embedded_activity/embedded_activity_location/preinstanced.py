__all__ = ('EmbeddedActivityLocationType', )

from ...bases import Preinstance as P, PreinstancedBase


class EmbeddedActivityLocationType(PreinstancedBase):
    """
    Represents an embedded activity location's type.
    
    Attributes
    ----------
    name : `str`
        The embedded activity location type's name.
    
    value : `str`
        The Discord side identifier value of the embedded activity location type.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`str`, ``EmbeddedActivityLocationType``) items
        Stores the predefined ``EmbeddedActivityLocationType``-s.
    
    VALUE_TYPE : `type` = `str`
        The embedded activity location types' values' type.
    
    DEFAULT_NAME : `str` = `''`
        The default name of the embedded activity location types. Guild features have the same value as name, so at their case it is not
        applicable.
    
    Every predefined embedded activity location type can be accessed as class attribute as well:
    
    +-----------------------+-------------------+---------------+
    | Class attribute names | name              | value         |
    +=======================+===================+===============+
    | none                  | none              |               |
    +-----------------------+-------------------+---------------+
    | guild_channel         | guild channel     | gc            |
    +-----------------------+-------------------+---------------+
    | private_channel       | private channel   | pc            |
    +-----------------------+-------------------+---------------+
    """
    INSTANCES = {}
    VALUE_TYPE = str
    DEFAULT_NAME = ''
    
    __slots__ = ()
    
    @classmethod
    def _from_value(cls, value):
        """
        Creates a new embedded activity location type.
        
        Parameters
        ----------
        value : `str`
            The embedded activity location type's identifier value.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.value = value
        self.name = value.casefold().replace('-', ' ')
        self.INSTANCES[value] = self
        return self
    
    
    # predefined
    none = P('', 'none')
    guild_channel = P('gc', 'guild channel')
    private_channel = P('pc', 'private channel')
