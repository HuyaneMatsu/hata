__all__ = ('Integration', )

import warnings

from scarletio import copy_docs, export

from ...bases import DiscordEntity
from ...core import INTEGRATIONS
from ...preconverters import preconvert_snowflake
from ...role import create_partial_role_from_id
from ...user import ZEROUSER

from ..integration_metadata import IntegrationMetadataBase, IntegrationMetadataSubscription

from .fields import (
    parse_enabled, parse_name, parse_type, parse_user, put_enabled_into, put_name_into, put_type_into, put_user_into,
    validate_enabled, validate_name, validate_type, validate_user
)
from .preinstanced import IntegrationType


@export
class Integration(DiscordEntity, immortal = True):
    """
    Represents a Discord Integration.
    
    Attributes
    ----------
    id : `int`
        The unique identifier number of the integration.
    enabled : `bool`
        Whether this integration is enabled.
    name : `str`
        The name of the integration.
    metadata : ``IntegrationMetadataBase``
        type specific information of the integration.
    type : ``IntegrationType``
        The type of the integration.
    user : ``ClientUserBase``
        User for who the integration is.
    """
    __slots__ = ('enabled', 'name', 'metadata', 'type', 'user')
    
    def __new__(
        cls,
        *,
        integration_type = ...,
        enabled = ...,
        name = ...,
        user = ...,
        **keyword_parameters,
    ):
        """
        Creates a new integration from the given keyword parameters.
        
        Parameters
        ----------
        integration_type : `str`, ``IntegrationType``, Optional (Keyword only)
            The integration's type.
        
        enabled : `bool`, Optional (Keyword only)
            Whether this integration is enabled.
        
        name : `str`, Optional (Keyword only)
            The name of the integration.
        
        user : ``ClientUserBase``, Optional (Keyword only)
            User for who the integration is.
        
        **keyword_parameters : Keyword parameters
            keyword parameters to set the integration's attributes as.
        
        Other Parameters
        ----------------
        account : ``IntegrationAccount``, ``ClientUserBase``, Optional (Keyword only)
            The integration's respective account. If the integration type is `'discord'`, then set as a discord user
            itself.
        
        application : ``IntegrationApplication``, Optional (Keyword only)
            The application of the integration if applicable.
        
        expire_behavior : `int`, ``IntegrationExpireBehavior``, Optional (Keyword only)
            The behavior of expiring subscription.
        
        expire_grace_period : `int`, Optional (Keyword only)
            The grace period in days for expiring subscribers.
        
        role_id : `int`, Optional (Keyword only)
            The role's identifier what the integration uses for subscribers.
        
        scopes : `None`, `iterable` of (`str`, ``Oauth2Scope``) items, Optional (Keyword only)
            The scopes the application was authorized with.
        
        subscriber_count : `int`, Optional (Keyword only)
            How many subscribers the integration has. 
        
        synced_at : `None`, `datetime`, Optional (Keyword only)
            When the integration was last synced.
        
        syncing : `bool`, Optional (Keyword only)
            Whether the integration syncing.
        
        Returns
        -------
        self : `instance<cls>`
        
        Raises
        ------
        TypeError
            - Parameter type incorrect.
            - Extra or unused parameters.
        ValueError
            - Parameter value incorrect.
        """
        # integration_type
        if integration_type is ...:
            integration_type = IntegrationType.none
        else:
            integration_type = validate_type(integration_type)
        
        # enabled
        if enabled is ...:
            enabled = False
        else:
            enabled = validate_enabled(enabled)
        
        # name
        if name is ...:
            name = ''
        else:
            name = validate_name(name)
        
        # user
        if user is ...:
            user = ZEROUSER
        else:
            user = validate_user(user)
        
        metadata = integration_type.metadata_type.from_keyword_parameters(keyword_parameters)
            
        if keyword_parameters:
            raise TypeError(
                f'Extra or unused keyword parameters: {keyword_parameters!r}.'
            )
        
        self = object.__new__(cls)
        self.id = 0
        self.enabled = enabled
        self.name = name
        self.metadata = metadata
        self.type = integration_type
        self.user = user
        return self
    
    
    @classmethod
    def precreate(cls, integration_id, *, integration_type = ..., **keyword_parameters):
        """
        Parameters
        ----------
        integration_id : `int`
            The integration's identifier.
        
        integration_type : `str`, ``IntegrationType``, Optional (Keyword only)
            The integration's type.
        
        **keyword_parameters : Keyword parameters
            keyword parameters to set the integration's attributes as.
        
        Other Parameters
        ----------------
        account : ``IntegrationAccount``, ``ClientUserBase``, Optional (Keyword only)
            The integration's respective account. If the integration type is `'discord'`, then set as a discord user
            itself.
        
        application : ``IntegrationApplication``, Optional (Keyword only)
            The application of the integration if applicable.
        
        enabled : `bool`, Optional (Keyword only)
            Whether this integration is enabled.
        
        expire_behavior : `int`, ``IntegrationExpireBehavior``, Optional (Keyword only)
            The behavior of expiring subscription.
        
        expire_grace_period : `int`, Optional (Keyword only)
            The grace period in days for expiring subscribers.
        
        name : `str`, Optional (Keyword only)
            The name of the integration.
        
        role_id : `int`, Optional (Keyword only)
            The role's identifier what the integration uses for subscribers.
        
        scopes : `None`, `iterable` of (`str`, ``Oauth2Scope``) items, Optional (Keyword only)
            The scopes the application was authorized with.
        
        subscriber_count : `int`, Optional (Keyword only)
            How many subscribers the integration has. 
        
        synced_at : `None`, `datetime`, Optional (Keyword only)
            When the integration was last synced.
        
        syncing : `bool`, Optional (Keyword only)
            Whether the integration syncing.
        
        user : ``ClientUserBase``, Optional (Keyword only)
            User for who the integration is.
        
        Returns
        -------
        self : `instance<cls>`
        
        Raises
        ------
        TypeError
            - Parameter type incorrect.
            - Extra or unused parameters.
        ValueError
            - Parameter value incorrect.
        """
        integration_id = preconvert_snowflake(integration_id, 'integration_id')
        
        if (integration_type is not ...) or keyword_parameters:
            processable = []
            
            if integration_type is ...:
                integration_type = IntegrationType.none
            else:
                integration_type = validate_type(integration_type)
            processable.append(('type', integration_type))
            
            # enabled
            try:
                enabled = keyword_parameters.pop('enabled')
            except KeyError:
                pass
            else:
                enabled = validate_enabled(enabled)
                processable.append(('enabled', enabled))
            
            # name
            try:
                name = keyword_parameters.pop('name')
            except KeyError:
                pass
            else:
                name = validate_name(name)
                processable.append(('name', name))
            
            # metadata
            metadata = integration_type.metadata_type.from_keyword_parameters(keyword_parameters)
            processable.append(('metadata', metadata))
            
            # user
            try:
                user = keyword_parameters.pop('user')
            except KeyError:
                pass
            else:
                user = validate_user(user)
                processable.append(('user', user))
            
            if keyword_parameters:
                raise TypeError(
                    f'Extra or unused keyword parameters: {keyword_parameters!r}.'
                )
        
        else:
            processable = None
        
        try:
            self = INTEGRATIONS[integration_id]
        except KeyError:
            self = cls._create_empty(integration_id)
            INTEGRATIONS[integration_id] = self
        
        else:
            if not self.partial:
                return self
        
        if (processable is not None):
            for item in processable:
                setattr(self, *item)
        
        return self
    
    
    @classmethod
    def _create_empty(cls, integration_id):
        """
        Creates a new integration with it's default attributes set.
        
        Parameters
        ----------
        integration_id : `int`
            The integration's identifier.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.id = integration_id
        self.enabled = True
        self.name = ''
        self.metadata = IntegrationMetadataBase._create_empty()
        self.type = IntegrationType.none
        self.user = ZEROUSER
        return self
    
    
    @classmethod
    def _create_with_role(cls, integration_id, role_id):
        """
        Creates a new integration with the given `role`.
        
        Parameters
        ----------
        integration_id : `int`
            The integration's identifier.
        role_id : `int`
            The role's identifier to create the integration with.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = cls._create_empty(integration_id)
        
        if role_id:
            self.metadata = IntegrationMetadataSubscription.from_role(role_id)
        
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new integration object with the given data. If the integration already exists, then updates and
        returns that instead.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Integration data received from Discord.
        
        Returns
        -------
        integration : `instance<cls>`
        """
        integration_id = int(data['id'])
        
        try:
            self = INTEGRATIONS[integration_id]
        except KeyError:
            self = object.__new__(cls)
            self.id = integration_id
            self._set_attributes(data)
            
            INTEGRATIONS[integration_id] = self
        
        else:
            self._set_attributes(data)
        
        return self
    
    
    def to_data(self, *, defaults = False, include_internals = False):
        """
        Converts the integration into a json serializable object.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default fields should be included as well.
        include_internals : `bool` = `False`, Optional (Keyword only)
            Whether internal fields should be included as well.
        
        Returns
        -------
        data : `dict` of (`str`, `Any`) items
        """
        # metadata
        data = self.metadata.to_data(defaults = defaults)
        
        # id
        if include_internals:
            data['id'] = str(self.id)
        
        # enabled
        put_enabled_into(self.enabled, data, defaults)
        
        # name
        put_name_into(self.name, data, defaults)
        
        # type
        put_type_into(self.type, data, defaults)
        
        # user
        if include_internals:
            put_user_into(self.user, data, defaults, include_internals = include_internals)
        
        return data
    
    
    def _set_attributes(self, data):
        """
        Sets the attributes of the integration from the given `data`.
        
        > `.id` field should be set already.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Integration data received from Discord.
        """
        integration_type = parse_type(data)
        
        self.enabled = parse_enabled(data)
        self.name = parse_name(data)
        self.metadata = integration_type.metadata_type.from_data(data)
        self.type = integration_type
        self.user = parse_user(data)
        
        return self
    
    
    @property
    def partial(self):
        """
        Returns whether the integration is partial.
        
        Returns
        -------
        partial : `bool`
        """
        if not self.id:
            return True
        
        if self.type is IntegrationType.none:
            return True
        
        return False
    
    
    def __repr__(self):
        """Returns the integration's representation."""
        repr_parts = ['<', self.__class__.__name__, ' id = ', str(self.id)]
        
        type_ = self.type
        if type_ is not IntegrationType.none:
            repr_parts.append(', type = ')
            repr_parts.append(repr(type_))
        
        user = self.user
        if (user is not ZEROUSER):
            repr_parts.append(', user = ')
            repr_parts.append(repr(user.full_name))
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)
    
    
    @copy_docs(DiscordEntity.__hash__)
    def __hash__(self):
        id_ = self.id
        if id_:
            return id_
        
        return self._get_hash_partial()
    
    
    def _get_hash_partial(self):
        """
        Hashes the fields of the integration.
        
        Returns
        -------
        hash_value : `int`
        """
        hash_value = 0
        
        # enabled
        hash_value ^= self.enabled << 2
        
        # name
        hash_value ^= hash(self.name)
        
        # metadata
        hash_value ^= hash(self.metadata)
        
        # type
        integration_type = self.type
        if (integration_type is not IntegrationType.none):
            hash_value ^= hash(integration_type)
        
        # user
        user = self.user
        if (user is not ZEROUSER):
            hash_value ^= hash(user)
        
        return hash_value
    

    def __eq__(self, other):
        """Returns whether the two integrations are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return self._is_equal_same_type(other)
    

    def __ne__(self, other):
        """Returns whether the two integrations are not equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return not self._is_equal_same_type(other)
    
    
    def _is_equal_same_type(self, other):
        """
        Returns whether the two integrations are equal.
        
        Helper method for ``.__eq__``
        
        Parameters
        ----------
        other : `instance<type<cls>>`
            The other instance. Must be from the same type.
        
        Returns
        -------
        is_equal : `bool`
        """
        self_id = self.id
        other_id = other.id
        if self_id and other_id:
            return self_id == other_id
        
        # enabled
        if self.enabled != other.enabled:
            return False
        
        # name
        if self.name != other.name:
            return False
        
        # metadata
        if self.metadata != other.metadata:
            return False
        
        # type
        if self.type != other.type:
            return False
        
        # user
        if self.user != other.user:
            return False
        
        return True
    
    
    def copy(self):
        """
        Copies the integration.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.id = 0
        new.enabled = self.enabled
        new.name = self.name
        new.metadata = self.metadata.copy()
        new.type = self.type
        new.user = self.user
        return new
    
    
    def copy_with(
        self,
        *,
        integration_type = ...,
        enabled = ...,
        name = ...,
        user = ...,
        **keyword_parameters,
    ):
        """
        Copies the integration account with the given fields.
        
        Parameters
        ----------
        integration_type : `str`, ``IntegrationType``, Optional (Keyword only)
            The integration's type.
        
        enabled : `bool`, Optional (Keyword only)
            Whether this integration is enabled.
        
        name : `str`, Optional (Keyword only)
            The name of the integration.
        
        user : ``ClientUserBase``, Optional (Keyword only)
            User for who the integration is.
        
        **keyword_parameters : Keyword parameters
            keyword parameters to set the integration's attributes as.
        
        Other Parameters
        ----------------
        account : ``IntegrationAccount``, ``ClientUserBase``, Optional (Keyword only)
            The integration's respective account. If the integration type is `'discord'`, then set as a discord user
            itself.
        
        application : ``IntegrationApplication``, Optional (Keyword only)
            The application of the integration if applicable.
        
        expire_behavior : `int`, ``IntegrationExpireBehavior``, Optional (Keyword only)
            The behavior of expiring subscription.
        
        expire_grace_period : `int`, Optional (Keyword only)
            The grace period in days for expiring subscribers.
        
        role_id : `int`, Optional (Keyword only)
            The role's identifier what the integration uses for subscribers.
        
        scopes : `None`, `iterable` of (`str`, ``Oauth2Scope``) items, Optional (Keyword only)
            The scopes the application was authorized with.
        
        subscriber_count : `int`, Optional (Keyword only)
            How many subscribers the integration has. 
        
        synced_at : `None`, `datetime`, Optional (Keyword only)
            When the integration was last synced.
        
        syncing : `bool`, Optional (Keyword only)
            Whether the integration syncing.
        
        Returns
        -------
        self : `instance<cls>`
        
        Raises
        ------
        TypeError
            - Parameter type incorrect.
            - Extra or unused parameters.
        ValueError
            - Parameter value incorrect.
        """
        # integration_type
        if integration_type is ...:
            integration_type = self.type
        else:
            integration_type = validate_type(integration_type)
        
        # enabled
        if enabled is ...:
            enabled = self.enabled
        else:
            enabled = validate_enabled(enabled)
        
        # name
        if name is ...:
            name = self.name
        else:
            name = validate_name(name)
        
        # user
        if user is ...:
            user = self.user
        else:
            user = validate_user(user)
        
        # metadata
        if integration_type is self.type:
            metadata = self.metadata.copy_with_keyword_parameters(keyword_parameters)
        else:
            metadata = integration_type.metadata_type.from_keyword_parameters(keyword_parameters)
        
        if keyword_parameters:
            raise TypeError(
                f'Extra or unused keyword parameters: {keyword_parameters!r}.'
            )
        
        new = object.__new__(type(self))
        new.id = 0
        new.enabled = enabled
        new.name = name
        new.metadata = metadata
        new.type = integration_type
        new.user = user
        return new
    
    
    @property
    def detail(self):
        """
        ``Integration.detail`` is deprecated and will be removed in 2023 February. Please use ``.metadata`` instead.
        """
        warnings.warn(
            (
                f'`{self.__class__.__name__}.detail` is deprecated and will be removed in 2023 February. '
                f'Please use `.metadata` instead.'
            ),
            FutureWarning,
            stacklevel = 2,
        )
        
        return self.metadata
    
    
    @property
    def role(self):
        """
        Returns the integration's role.
        
        Returns
        -------
        role : `None`, ``Role``
        """
        role_id = self.role_id
        if role_id:
            return create_partial_role_from_id(role_id)
    
    # Metadata proxy properties
    
    @property
    @copy_docs(IntegrationMetadataBase.account)
    def account(self):
        return self.metadata.account
    
    
    @property
    @copy_docs(IntegrationMetadataBase.application)
    def application(self):
        return self.metadata.application
    
    
    @property
    @copy_docs(IntegrationMetadataBase.expire_behavior)
    def expire_behavior(self):
        return self.metadata.expire_behavior
    
    
    @property
    @copy_docs(IntegrationMetadataBase.expire_grace_period)
    def expire_grace_period(self):
        return self.metadata.expire_grace_period
    
    
    @property
    @copy_docs(IntegrationMetadataBase.revoked)
    def revoked(self):
        return self.metadata.revoked
    
    
    @property
    @copy_docs(IntegrationMetadataBase.role_id)
    def role_id(self):
        return self.metadata.role_id
    
    
    @property
    @copy_docs(IntegrationMetadataBase.scopes)
    def scopes(self):
        return self.metadata.scopes
    
    
    @property
    @copy_docs(IntegrationMetadataBase.subscriber_count)
    def subscriber_count(self):
        return self.metadata.subscriber_count
    
    
    @property
    @copy_docs(IntegrationMetadataBase.synced_at)
    def synced_at(self):
        return self.metadata.synced_at
    
    
    @property
    @copy_docs(IntegrationMetadataBase.syncing)
    def syncing(self):
        return self.metadata.syncing
