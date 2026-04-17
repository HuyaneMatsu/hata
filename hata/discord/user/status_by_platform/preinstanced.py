__all__ = ('SessionPlatformType', 'Status', )

from scarletio import copy_docs

from ...bases import Preinstance as P, PreinstancedBase


class Status(PreinstancedBase, value_type = str):
    """
    Represents a Discord user's status.
    
    Attributes
    ----------
    name : `str`
        The status's name.
    
    position : `int`
        Internal position of the status for sorting purposes.
    
    value : `str`
        The identifier value of the status.
    
    Type Attributes
    ---------------
    Each predefined status also can be accessed as a type attribute:
    
    +-----------------------+-----------+-----------+
    | Type attribute name   | position  | value     |
    +=======================+===========+===========+
    | online                | 0         | idle      |
    +-----------------------+-----------+-----------+
    | idle                  | 1         | idle      |
    +-----------------------+-----------+-----------+
    | dnd                   | 2         | dnd       |
    +-----------------------+-----------+-----------+
    | offline               | 3         | offline   |
    +-----------------------+-----------+-----------+
    | invisible             | 3         | invisible |
    +-----------------------+-----------+-----------+
    """
    __slots__ = ('position', )
    
    def __new__(cls, value, name = None, position = 4):
        """
        Creates a new status.
        
        Parameters
        ----------
        value : `str`
            The identifier value of the status.
        
        name : `None | str` = `None`, Optional
            The status's name.
        
        position : `int = `4`, Optional
            Internal position of the status for sorting purposes.
        """
        if name is None:
            name = value
        
        self = PreinstancedBase.__new__(cls, value, name)
        self.position = position
        return self
    
    
    @copy_docs(PreinstancedBase.__lt__)
    def __lt__(self, other):
        if self is other:
            return False
        
        self_type = type(self)
        other_type = type(other)
        if self_type is other_type:
            pass
        
        elif issubclass(other_type, self_type.VALUE_TYPE):
            try:
                other = self_type.INSTANCES[other]
            except KeyError:
                return True
        
        else:
            return NotImplemented
        
        self_position = self.position
        other_position = other.position
        
        if self_position < other_position:
            return True
        
        if self_position > other_position:
            return False
        
        return (self.value < other.value)
    
    
    @copy_docs(PreinstancedBase.__gt__)
    def __gt__(self, other):
        if self is other:
            return False
        
        self_type = type(self)
        other_type = type(other)
        if self_type is other_type:
            pass
        
        elif issubclass(other_type, self_type.VALUE_TYPE):
            try:
                other = self_type.INSTANCES[other]
            except KeyError:
                return False
        
        else:
            return NotImplemented
        
        self_position = self.position
        other_position = other.position
        
        if self_position > other_position:
            return True
        
        if self_position < other_position:
            return False
        
        return (self.value > other.value)
    
    
    @copy_docs(PreinstancedBase.__eq__)
    def __eq__(self, other):
        if self is other:
            return True
        
        self_type = type(self)
        other_type = type(other)
        if self_type is other_type:
            pass
        
        elif issubclass(other_type, self_type.VALUE_TYPE):
            try:
                other = self_type.INSTANCES[other]
            except KeyError:
                return False
        
        else:
            return NotImplemented
    
        if self.position != other.position:
            return False
        
        if self.value != other.value:
            return False
        
        return True
    
    
    # predefined
    online = P('online', 'online', 0)
    idle = P('idle', 'idle', 1)
    dnd = P('dnd', 'dnd', 2)
    offline = P('offline', 'offline', 3)
    invisible = P('invisible', 'invisible', 3)


# Set default status
Status.INSTANCES[''] = Status.offline


class SessionPlatformType(PreinstancedBase, value_type = str):
    """
    Represents a session's platform type a user is logged in from.
    
    Attributes
    ----------
    name : `str`
        The name of the session platform type.
    
    value : `str`
        The Discord side identifier value of the session platform type.
    
    Type Attributes
    ---------------
    Every predefined session platform type can also be accessed as type attribute:
    
    +-----------------------+---------------+-----------+
    | Type attribute name   | name          | value     |
    +=======================+===============+===========+
    | none                  | none          |           |
    +-----------------------+---------------+-----------+
    | desktop               | desktop       | desktop   |
    +-----------------------+---------------+-----------+
    | embedded              | embedded      | embedded  |
    +-----------------------+---------------+-----------+
    | mobile                | mobile        | mobile    |
    +-----------------------+---------------+-----------+
    | web                   | web           | web       |
    +-----------------------+---------------+-----------+
    """
    __slots__ = ()

    # predefined
    none = P('', 'none')
    desktop = P('desktop', 'desktop')
    embedded = P('embedded', 'embedded')
    mobile = P('mobile', 'mobile')
    web = P('web', 'web')
