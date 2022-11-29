__all__ = ('ApplicationInstallParameters',)

from scarletio import RichAttributeErrorBaseType

from ...permission import Permission

from .fields import (
    parse_permissions, parse_scopes, put_permissions_into, put_scopes_into, validate_permissions, validate_scopes
)


class ApplicationInstallParameters(RichAttributeErrorBaseType):
    """
    Parameters for inviting a bot.
    
    Attributes
    ----------
    permissions : ``Permission``
        The permissions to invite the bot with.
    scopes : `None`, `tuple` of `str`
        Oauth2 scopes to invite the bot with.
    """
    __slots__ = ('permissions', 'scopes')
    
    def __new__(cls, *, permissions = ..., scopes = ...):
        """
        Creates a new application install parameters.
        
        Parameters
        ----------
        permissions : `int`, ``Permission``, Optional (Keyword only)
            The permissions to invite the bot with.
        
        scopes : `None`, `iterable` of (``Oauth2Scope``, `str`), Optional (Keyword only)
            Oauth2 scopes to invite the bot with.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        if permissions is ...:
            permissions = Permission()
        else:
            permissions = validate_permissions(permissions)
        
        if scopes is ...:
            scopes = None
        else:
            scopes = validate_scopes(scopes)
        
        self = object.__new__(cls)
        self.permissions = permissions
        self.scopes = scopes
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a application installation parameters instance from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Application installation parameters data.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.scopes = parse_scopes(data)
        self.permissions = parse_permissions(data)
        return self
    
    
    def to_data(self, *, defaults = False):
        """
        Converts the application install parameters to json serializable object.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether fields with their default value should be included as well.
        
        Returns
        -------
        data : `dict` of (`str`, `Any`) items
        """
        data = {}
        put_permissions_into(self.permissions, data, defaults)
        put_scopes_into(self.scopes, data, defaults)
        return data
    
    
    def __repr__(self):
        """Returns the application install parameters' representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' scopes = [')
        
        scopes = self.scopes
        if (scopes is not None):
            length = len(scopes)
            index = 0
            
            while True:
                scope = scopes[index]
                repr_parts.append(repr(scope))
                
                index += 1
                if index == length:
                    break
                
                repr_parts.append(', ')
                continue
        
        repr_parts.append(']')
        
        repr_parts.append(', permissions = ')
        repr_parts.append(format(self.permissions, 'd'))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __hash__(self):
        """Returns the application install parameters' hash value."""
        hash_value = 0
        
        scopes = self.scopes
        if (scopes is not None):
            hash_value ^= len(scopes) << 16
            
            for scope in scopes:
                hash_value ^= hash(scope)
        
        hash_value ^= self.permissions
        
        return hash_value
    
    
    def __eq__(self, other):
        """Returns whether the two application install parameters are equal."""
        if type(other) is not ApplicationInstallParameters:
            return NotImplemented
        
        if self.permissions != other.permissions:
            return False
        
        if self.scopes != other.scopes:
            return False
        
        return True
    
    
    def copy(self):
        """
        Copies the application install parameters.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.permissions = self.permissions
        scopes = self.scopes
        if (scopes is not None):
            scopes = (*scopes, )
        new.scopes = scopes
        return new

    
    def copy_with(self, permissions = ..., scopes = ...):
        """
        Copies the application install parameters with the given fields.
        
        Parameters
        ----------
        permissions : `int`, ``Permission``, Optional (Keyword only)
            The permissions to invite the bot with.
        
        scopes : `None`, `iterable` of (``Oauth2Scope``, `str`), Optional (Keyword only)
            Oauth2 scopes to invite the bot with.
        
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
        if permissions is ...:
            permissions = self.permissions
        else:
            permissions = validate_permissions(permissions)
        
        if scopes is ...:
            scopes = self.scopes
            if (scopes is not None):
                scopes = (*scopes, )
        else:
            scopes = validate_scopes(scopes)
        
        new = object.__new__(type(self))
        new.permissions = permissions
        new.scopes = scopes
        return new
