__all__ = ('IntegrationMetadataDiscord',)

from scarletio import copy_docs

from ..integration_account import IntegrationAccount

from .base import IntegrationMetadataBase
from .fields import (
    parse_account__discord, parse_application, put_account_into__discord, put_application_into,
    validate_account__discord, validate_application
)


class IntegrationMetadataDiscord(IntegrationMetadataBase):
    """
    Integration metadata for discord integrations.
    
    Attributes
    ----------
    account : ``IntegrationAccount``, ``ClientUserBase``
        The invited bot.
    application : `None`, ``IntegrationApplication``
        The bot's application.
    """
    __slots__ = ('account', 'application',)
    
    def __new__(cls, *, account = ..., application = ...):
        """
        Creates a new discord integration metadata instance with the given parameters.
        
        Parameters
        ----------
        account : ``IntegrationAccount``, ``ClientUserBase``, Optional (Keyword only)
            The invited bot.
        application : `None`, ``IntegrationApplication``, Optional (Keyword only)
            The bot's application.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # account
        if account is ...:
            account = IntegrationAccount._create_empty()
        else:
            account = validate_account__discord(account)
        
        # application
        if application is ...:
            application = None
        else:
            application = validate_application(application)
        
        # Construct
        self = object.__new__(cls)
        self.account = account
        self.application = application
        return self
    
    
    @classmethod
    @copy_docs(IntegrationMetadataBase.from_keyword_parameters)
    def from_keyword_parameters(cls, keyword_parameters):
        return cls(
            account = keyword_parameters.pop('account', ...),
            application = keyword_parameters.pop('application', ...),
        )
    
    
    @copy_docs(IntegrationMetadataBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
        if self.account != other.account:
            return False
        
        if self.application != other.application:
            return False
        
        return True
    
    
    @copy_docs(IntegrationMetadataBase.__hash__)
    def __hash__(self):
        hash_value = 0
        
        # account
        hash_value ^= hash(self.account)
        
        # application
        application = self.application
        if (application is not None):
            hash_value ^= hash(application)
        
        return hash_value
    
    
    @classmethod
    @copy_docs(IntegrationMetadataBase._create_empty)
    def _create_empty(cls):
        self = object.__new__(cls)
        self.account = IntegrationAccount._create_empty()
        self.application = None
        return self
    
    
    @classmethod
    @copy_docs(IntegrationMetadataBase.from_data)
    def from_data(cls, data):
        self = object.__new__(cls)
        self.account = parse_account__discord(data)
        self.application = parse_application(data)
        return self
    
    
    @copy_docs(IntegrationMetadataBase.to_data)
    def to_data(self, *, defaults = False):
        data = {}
        put_account_into__discord(self.account, data, defaults)
        put_application_into(self.application, data, defaults)
        return data
    
    
    @copy_docs(IntegrationMetadataBase.copy)
    def copy(self):
        new = object.__new__(type(self))
        new.account = self.account
        new.application = self.application
        return new
    
    
    def copy_with(self, *, account = ..., application = ...):
        """
        Copies the discord integration metadata with the given fields.
        
        Creates a new discord integration metadata instance with the given parameters.
        
        Parameters
        ----------
        account : ``IntegrationAccount``, ``ClientUserBase``, Optional (Keyword only)
            The invited bot.
        application : `None`, ``IntegrationApplication``, Optional (Keyword only)
            The bot's application.
        
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
        # account
        if account is ...:
            account = self.account
        else:
            account = validate_account__discord(account)
        
        # application
        if application is ...:
            application = self.application
        else:
            application = validate_application(application)
        
        self = object.__new__(type(self))
        self.account = account
        self.application = application
        return self
    
    
    @copy_docs(IntegrationMetadataBase.copy_with_keyword_parameters)
    def copy_with_keyword_parameters(self, keyword_parameters):
        return self.copy_with(
            account = keyword_parameters.pop('account', ...),
            application = keyword_parameters.pop('application', ...),
        )
