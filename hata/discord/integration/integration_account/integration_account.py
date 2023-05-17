__all__ = ('IntegrationAccount', )

from scarletio import RichAttributeErrorBaseType

from .fields import parse_name, parse_id, validate_name, validate_id, put_name_into, put_id_into


class IntegrationAccount(RichAttributeErrorBaseType):
    """
    Account for who an ``Integration`` is for.
    
    Attributes
    ----------
    id : `str`
        The respective account's identifier.
    name : `str`
        The respective account's name.
    """
    __slots__ = ('id', 'name', )
    
    def __new__(cls, integration_account_id = ..., name = ...):
        """
        Creates a new integration account instance from the given account data and integration type.
        
        Parameters
        ----------
        integration_account_id : `None`, `str`, Optional
            The integration account's identifier.
        name : `None`, `str`, Optional
            The integration account's name.
        
        Returns
        -------
        self : `instance<cls>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # integration_account_id
        if integration_account_id is ...:
            integration_account_id = ''
        else:
            integration_account_id = validate_id(integration_account_id)
        
        # name
        if name is ...:
            name = ''
        else:
            name = validate_name(name)
        
        self = object.__new__(cls)
        self.id = integration_account_id
        self.name = name
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new integration account instance from the given account data and integration type.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Integration account data.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.id = parse_id(data)
        self.name = parse_name(data)
        return self
    
    
    def to_data(self, *, defaults = False):
        """
        Converts the integration account into a json serializable object.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default field values should be included as well.
        
        Returns
        -------
        data : `dict` of (`str`, `object`) items
        """
        data = {}
        put_id_into(self.id, data, defaults)
        put_name_into(self.name, data, defaults)
        return data
    
    
    def __repr__(self):
        """Returns the integration account's representation."""
        return f'<{self.__class__.__name__} id = {self.id!r}, name = {self.name!r}>'
    
    
    def __eq__(self, other):
        """Returns whether the two integration accounts are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.id != other.id:
            return False
        
        if self.name != other.name:
            return False
        
        return True
    
    
    def __hash__(self):
        """Returns the hash value of the integration account."""
        hash_value = 0
        
        # id
        hash_value ^= hash(self.id)
        
        # name
        hash_value ^= hash(self.name)
        
        return hash_value
    
    
    @classmethod
    def _create_empty(cls):
        """
        Creates an empty integration account, with it's attributes set as empty strings.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.id = ''
        self.name = ''
        return self
    
    
    def copy(self):
        """
        Copies the integration application returning a new one.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.id = self.id
        new.name = self.name
        return new
    

    def copy_with(self, *, integration_account_id = ..., name = ...):
        """
        Copies the integration application with the given fields.
        
        Parameters
        ----------
        integration_account_id : `None`, `str`, Optional (Keyword only)
            The integration account's identifier.
        name : `None`, `str`, Optional (Keyword only)
            The integration account's name.
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
        # integration_account_id
        if integration_account_id is ...:
            integration_account_id = self.id
        else:
            integration_account_id = validate_id(integration_account_id)
        
        # name
        if name is ...:
            name = self.name
        else:
            name = validate_name(name)
        
        new = object.__new__(type(self))
        new.id = integration_account_id
        new.name = name
        return new
