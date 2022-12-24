__all__ = ('WelcomeScreen',)

import reprlib

from scarletio import RichAttributeErrorBaseType

from .fields import (
    parse_description, parse_welcome_channels, put_description_into, put_welcome_channels_into, validate_description,
    validate_welcome_channels
)


class WelcomeScreen(RichAttributeErrorBaseType):
    """
    Represents a guild's welcome screen.
    
    Attributes
    ----------
    description : `None`, `str`
        Description, of what is the server about.
    welcome_channels : `None`, `tuple` of ``WelcomeScreenChannel``
        The featured channels by the welcome screen.
    """
    __slots__ = ('description', 'welcome_channels', )
    
    def __new__(cls, *, description = ..., welcome_channels = ...):
        """
        Creates a new welcome screen.
        
        Parameters
        ----------
        description : `None`, `str`, Optional (Keyword only)
            Description, of what is the server about.
        welcome_channels : `None`, `iterable` of ``WelcomeScreenChannel``, Optional (Keyword only)
            The featured channels by the welcome screen.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # description
        if description is ...:
            description = None
        else:
            description = validate_description(description)
        
        # welcome_channels
        if welcome_channels is ...:
            welcome_channels = None
        else:
            welcome_channels = validate_welcome_channels(welcome_channels)
        
        # Construct
        self = object.__new__(cls)
        self.description = description
        self.welcome_channels = welcome_channels
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new welcome screen instance from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Welcome screen data.
        """
        self = object.__new__(cls)
        self.description = parse_description(data)
        self.welcome_channels = parse_welcome_channels(data)
        return self
    
    
    def to_data(self, *, defaults = False):
        """
        Converts the welcome screen to a json serializable object.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether fields with their default values should be included as well.
        
        Returns
        -------
        data : `dict` of (`str`, `object`) items
        """
        data = {}
        put_description_into(self.description, data, defaults)
        put_welcome_channels_into(self.welcome_channels, data, defaults)
        return data
    
    
    def __repr__(self):
        """Returns the welcome screen's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        field_added = False
        
        # description
        description = self.description
        if (description is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' description = ')
            repr_parts.append(reprlib.repr(description))
        
        # welcome_channels
        welcome_channels = self.welcome_channels
        if (welcome_channels is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' welcome_channels = [')
            
            index = 0
            limit = len(welcome_channels)
            
            while True:
                welcome_channel = welcome_channels[index]
                
                repr_parts.append(repr(welcome_channel))
                
                index += 1
                if index == limit:
                    break
                
                repr_parts.append(', ')
                continue
            
            repr_parts.append(']')
            
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __hash__(self):
        """Returns the welcome screen's hash."""
        hash_value = 0
        
        # description
        description = self.description
        if (description is not None):
            hash_value ^= hash(description)
        
        welcome_channels = self.welcome_channels
        if (welcome_channels is not None):
            hash_value ^= len(welcome_channels)
            
            for welcome_channel in welcome_channels:
                hash_value ^= hash(welcome_channel)
        
        return hash_value
    
    
    def __eq__(self, other):
        """Returns whether the two welcome screens are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.description != other.description:
            return False
        
        if self.welcome_channels != other.welcome_channels:
            return False
        
        return True
    
    
    def copy(self):
        """
        Copies the welcome screen.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.description = self.description
        welcome_channels = self.welcome_channels
        if (welcome_channels is not None):
            welcome_channels = (*welcome_channels,)
        new.welcome_channels = welcome_channels
        return new
    
    
    def copy_with(self, *, description = ..., welcome_channels = ...):
        """
        Copies the welcome screen with the given fields.
        
        Parameters
        ----------
        description : `None`, `str`, Optional (Keyword only)
            Description, of what is the server about.
        welcome_channels : `None`, `iterable` of ``WelcomeScreenChannel``, Optional (Keyword only)
            The featured channels by the welcome screen.
        
        Returns
        -------
        new : `instance<type<self>>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # description
        if description is ...:
            description = self.description
        else:
            description = validate_description(description)
        
        # welcome_channels
        if welcome_channels is ...:
            welcome_channels = self.welcome_channels
            if (welcome_channels is not None):
                welcome_channels = (*welcome_channels,)
        else:
            welcome_channels = validate_welcome_channels(welcome_channels)
        
        # Construct
        self = object.__new__(type(self))
        self.description = description
        self.welcome_channels = welcome_channels
        return self
    
    
    def iter_welcome_channels(self):
        """
        Iterates over the welcome channels of the welcome screen.
        
        This method is an iterable generator.
        
        Yields
        ------
        welcome_channel : ``WelcomeScreenChannel``
        """
        welcome_channels = self.welcome_channels
        if (welcome_channels is not None):
            yield from welcome_channels
