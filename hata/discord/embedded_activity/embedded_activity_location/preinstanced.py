__all__ = ('EmbeddedActivityLocationType', )

from scarletio import copy_docs

from ...bases import Preinstance as P, PreinstancedBase


class EmbeddedActivityLocationType(PreinstancedBase, value_type = str):
    """
    Represents an embedded activity location's type.
    
    Attributes
    ----------
    name : `str`
        The embedded activity location type's name.
    
    value : `str`
        The Discord side identifier value of the embedded activity location type.
    
    Type Attributes
    ---------------
    Every predefined embedded activity location type can be accessed as type attribute as well:
    
    +-----------------------+-------------------+---------------+
    | Type attribute name   | name              | value         |
    +=======================+===================+===============+
    | none                  | none              |               |
    +-----------------------+-------------------+---------------+
    | guild_channel         | guild channel     | gc            |
    +-----------------------+-------------------+---------------+
    | private_channel       | private channel   | pc            |
    +-----------------------+-------------------+---------------+
    """
    __slots__ = ()
    
    @copy_docs(PreinstancedBase.__new__)
    def __new__(cls, value, name = None):
        if name is None:
            name = value.casefold().replace('-', ' ')
        
        return PreinstancedBase.__new__(cls, value, name)
    
    
    # predefined
    none = P('', 'none')
    guild_channel = P('gc', 'guild channel')
    private_channel = P('pc', 'private channel')
