__all__ = ('IntegrationAccount', )

from ..user import User

from .preinstanced import IntegrationType


INTEGRATION_TYPE_DISCORD = IntegrationType.discord


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
    
    def __new__(cls, data, integration_type):
        """
        Creates a new integration account instance from the given account data and integration type.
        
        If `integration_type` is `'discord'`, then returns a Discord user instead.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Integration account data.
        integration_type : ``IntegrationType``
            The parent integration's type.
        
        Returns
        -------
        self : ``IntegrationAccount``, ``ClientUserBase``
        """
        name = data['name']
        id_ = data['id']
        if integration_type is INTEGRATION_TYPE_DISCORD:
            return User.precreate(id_, name=name, bot=True)
        
        self = object.__new__(cls)
        self.name = name
        self.id = id_
        
        return self
    
    
    def __repr__(self):
        """Returns the integration account's representation."""
        return f'<{self.__class__.__name__} name={self.name!r}, id={self.id!r}>'
    
    
    @classmethod
    def _create_empty(cls):
        """
        Creates an empty integration account, with it's attributes set as empty strings.
        """
        self = object.__new__(cls)
        self.id = ''
        self.name = ''
        return self
