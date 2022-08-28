__all__ = ('Integration', )

from ..bases import DiscordEntity
from ..core import INTEGRATIONS
from ..oauth2.helpers import parse_oauth2_scope_array
from ..user import User, ZEROUSER

from .integration_account import IntegrationAccount
from .integration_application import IntegrationApplication
from .integration_detail import IntegrationDetail
from .preinstanced import IntegrationType


INTEGRATION_TYPE_DISCORD = IntegrationType.discord


class Integration(DiscordEntity, immortal=True):
    """
    Represents a Discord Integration.
    
    Attributes
    ----------
    id : `int`
        The unique identifier number of the integration.
    account : ``IntegrationAccount``, ``ClientUserBase``
        The integration's respective account. If the integration type is `'discord'`, then set as a discord user
        itself.
    application : `None`, ``Application``
        The application of the integration if applicable.
    enabled : `bool`
        Whether this integration is enabled.
    detail : ``IntegrationDetail``
        Additional integration information for non `'discord'` integrations.
    name : `str`
        The name of the integration.
    scopes : `None`, `tuple` of ``Oauth2Scope``
        The scopes the application was authorized with.
    type : ``IntegrationType``
        The type of the integration.
    user : `ClientUserBase`
        User for who the integration is. Defaults to `ZEROUSER`
    """
    __slots__ = ('account', 'application', 'detail', 'enabled', 'name', 'scopes', 'type', 'user')
    
    def __new__(cls, data):
        """
        Creates a new integration object with the given data. If the integration already exists, then updates and
        returns that instead.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Integration data received from Discord.
        
        Returns
        -------
        integration : ``Integration``
        """
        integration_id = int(data['id'])
        try:
            self = INTEGRATIONS[integration_id]
        except KeyError:
            self = object.__new__(cls)
            self.id = integration_id
            
            update = True
        else:
            update = False
        
        self.name = data['name']
        self.type = integration_type = IntegrationType.get(data['type'])
        
        if integration_type is INTEGRATION_TYPE_DISCORD:
            detail = None
        else:
            detail = IntegrationDetail(data)
        self.detail = detail
        
        self.enabled = data['enabled']
        
        user_data = data.get('user', None)
        if user_data is None:
            user = ZEROUSER
        else:
            user = User.from_data(user_data)
        self.user = user
        
        application_data = data.get('application', None)
        if application_data is None:
            application = None
        else:
            application = IntegrationApplication(application_data)
        
        if update:
            self.application = application
        else:
            if (application is not None):
                self.application = application
        
        self.scopes = parse_oauth2_scope_array(data.get('scopes', None))
        
        # Create account last, because it might create a ``User`` object, but ``.application`` might have included it
        # already.
        self.account = IntegrationAccount(data['account'], integration_type)
        
        return self
    
    
    @property
    def partial(self):
        """
        Returns whether the integration is partial.
        
        Returns
        -------
        partial : `bool`
        """
        return (not self.type)
    
    
    def __repr__(self):
        """Returns the integration's representation."""
        repr_parts = ['<', self.__class__.__name__, ' id=', str(self.id)]
        
        type_ = self.type
        if type_ is not IntegrationType.none:
            repr_parts.append(', type=')
            repr_parts.append(repr(type_))
        
        user = self.user
        if (user is not ZEROUSER):
            repr_parts.append(', user=')
            repr_parts.append(repr(user.full_name))
        
        detail = self.detail
        if (detail is not None):
            repr_parts.append(', detail=')
            repr_parts.append(repr(detail))
        
        application = self.application
        if (application is not None):
            repr_parts.append(', application')
            repr_parts.append(repr(application))
        
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)
