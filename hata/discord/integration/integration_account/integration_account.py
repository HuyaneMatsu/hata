__all__ = ('IntegrationAccount', )

from scarletio import include

from .fields import parse_name, parse_id, validate_name, validate_id, put_name_into, put_id_into


IntegrationType = include('IntegrationType')


class IntegrationAccount:
    """
    Account for who an ``Integration`` is for.
    
    Attributes
    ----------
    id : `str`
        The respective account's id.
    name : `str`
        The respective account's name.
    """
    __slots__ = ('id', 'name', )
    
    def __new__(cls, integration_account_id = None, name = None):
        """
        Creates a new integration account instance from the given account data and integration type.
        
        If `integration_type` is `'discord'`, then returns a Discord user instead.
        
        Parameters
        ----------
        integration_account_id : `None`, `str` = `None` Optional
            The integration account's identifier.
        name : `None`, `str` = `None`, Optional
            The integration account's name.
        
        Returns
        -------
        self : ``IntegrationAccount``, ``ClientUserBase``
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        integration_account_id = validate_id(integration_account_id)
        name = validate_name(name)
        
        self = object.__new__(cls)
        
        self.id = integration_account_id
        self.name = name
        
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new integration account instance from the given account data and integration type.
        
        If `integration_type` is `IntegrationType.discord`, then returns a Discord user instead.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Integration account data.
        
        Returns
        -------
        self : ``IntegrationAccount``
        """
        self = object.__new__(cls)
        
        self.id = parse_id(data)
        self.name = parse_name(data)
        
        return self
    
    
    def to_data(self, defaults = False):
        """
        Converts the integration account into a json serializable object.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default field values should be included as well.
        
        Returns
        -------
        data : `dict` of (`str`, `Any`) items
        """
        data = {}
        
        put_id_into(self.id, data, defaults)
        put_name_into(self.name, data, defaults)
        
        return data
    
    
    def __repr__(self):
        """Returns the integration account's representation."""
        return f'<{self.__class__.__name__} id={self.id!r}, name={self.name!r}>'
    
    
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
