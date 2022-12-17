__all__ = ('IntegrationMetadataBase',)

from scarletio import RichAttributeErrorBaseType

from ...bases import PlaceHolder

from ..integration_account import IntegrationAccount

from .constants import EXPIRE_GRACE_PERIOD_DEFAULT, SUBSCRIBER_COUNT_DEFAULT
from .preinstanced import IntegrationExpireBehavior


class IntegrationMetadataBase(RichAttributeErrorBaseType):
    """
    Base type specific metadata for integrations.
    """
    __all__ = ()
    
    def __eq__(self, other):
        """Returns whether the two integration accounts are the same."""
        if type(self) is not type(other):
            return False
        
        return self._is_equal_same_type(other)
    
    
    def _is_equal_same_type(self, other):
        """
        Returns whether the two integration metadatas are equal.
        
        > Both object must have the same type.
        
        Parameters
        ----------
        other : `instance<type<cls>>`
            The other instance.
        """
        return True
    
    
    def __hash__(self):
        """Returns the integration account's hash value."""
        return 0
    
    
    def __repr__(self):
        return f'<{self.__class__.__name__}>'
    
    
    def __new__(cls, keyword_parameters):
        """
        Creates a new integration metadata from the given keyword parameters.
        
        Parameters
        ----------
        keyword_parameters : `dict` of (`str`, `object`) items
            Keyword parameters to populate the attributes.
        
        The used fields are removed from `keyword_parameters`.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        return object.__new__(cls)
    
    
    @classmethod
    def _create_empty(cls):
        """
        Creates an empty integration metadata with it's default attributes set.
        
        Returns
        -------
        self : `instance<self>`
        """
        return object.__new__(cls)
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new integration metadata from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Integration data.
        
        Returns
        -------
        self : `instance<cls>`
        """
        return object.__new__(cls)
    
    
    def to_data(self, *, defaults = False):
        """
        Converts the integration metadata into json serializable object.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default fields should be included as well.
        
        Returns
        -------
        data : `dict` of (`str`, `object`) items
        """
        return {}
    
    
    def copy(self):
        """
        Returns a copy of the integration metadata.
        
        Returns
        -------
        copy : `instance<cls>`
        """
        return object.__new__(type(self))
    
    
    def copy_with(self, keyword_parameters):
        """
        Returns a copy of the integration metadata with using the given keyword parameters to populate it.
        
        The used fields are removed from `keyword_parameters`.
        
        Parameters
        ----------
        keyword_parameters : `dict` of (`str`, `object`) items
            Keyword parameters to populate the attributes.
        
        Returns
        -------
        copy : `instance<cls>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        return self.copy()
    
    
    account = PlaceHolder(
        IntegrationAccount._create_empty(),
        """
        The integration's respective account. If the integration type is `'discord'`, then set as a discord user
        itself.
        
        Returns
        -------
        account : ``IntegrationAccount``, ``ClientUserBase``
        """
    )
    
    
    application = PlaceHolder(
        None,
        """
        The application of the integration if applicable.
        
        Returns
        -------
        application : `None`, ``IntegrationApplication``
        """
    )
    
    
    expire_behavior = PlaceHolder(
        IntegrationExpireBehavior.remove_role,
        """
        The behavior of expiring subscription.
        
        Returns
        -------
        expire_behavior : ``IntegrationExpireBehavior``
        """
    )
    
    
    expire_grace_period = PlaceHolder(
        EXPIRE_GRACE_PERIOD_DEFAULT,
        """
        The grace period in days for expiring subscribers.
        
        Returns
        -------
        expire_grace_period : `int`
        """
    )
    
    
    revoked = PlaceHolder(
        False,
        """
        Whether the integration is removed.
        
        Returns
        -------
        revoked : `bool`
        """
    )
    
    
    role_id = PlaceHolder(
        0,
        """
        The role's identifier what the integration uses for subscribers.
        
        Returns
        -------
        role_id : `int`
        """
    )
    
    
    scopes = PlaceHolder(
        None,
        """
        The scopes the application was authorized with.
        
        Returns
        -------
        scopes : `None`, `tuple` of ``Oauth2Scope``
        """
    )
    
    
    subscriber_count = PlaceHolder(
        SUBSCRIBER_COUNT_DEFAULT,
        """
        How many subscribers the integration has. 
        
        Returns
        -------
        subscriber_count : `int`
        """
    )
    
    
    synced_at = PlaceHolder(
        None,
        """
        When the integration was last synced.
        
        synced_at : `None`, `datetime`
        """
    )
    
    
    syncing = PlaceHolder(
        False,
        """
        Whether the integration syncing.
        
        Returns
        -------
        syncing : `bool`
        """
    )
