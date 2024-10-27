__all__ = ('InteractionEvent',)

from scarletio import Future, copy_docs, export, include, shield

from ...bases import DiscordEntity, EventBase
from ...channel import Channel, ChannelType, create_partial_channel_from_id
from ...core import (
    APPLICATION_ID_TO_CLIENT, INTERACTION_EVENT_MESSAGE_WAITERS, INTERACTION_EVENT_RESPONSE_WAITERS, KOKORO
)
from ...localization.utils import LOCALE_DEFAULT
from ...message import Message
from ...permission import Permission
from ...precreate_helpers import process_precreate_parameters, raise_extra
from ...user import ClientUserBase, ZEROUSER, create_partial_user_from_id
from ...utils import now_as_id

from ..interaction_metadata import InteractionMetadataBase
from ..responding.constants import (
    RESPONSE_FLAG_ACKNOWLEDGED, RESPONSE_FLAG_ACKNOWLEDGING, RESPONSE_FLAG_DEFERRED, RESPONSE_FLAG_DEFERRING,
    RESPONSE_FLAG_EPHEMERAL, RESPONSE_FLAG_NONE, RESPONSE_FLAG_RESPONDED, RESPONSE_FLAG_RESPONDING
)

from .constants import DEFAULT_INTERACTION_METADATA, INTERACTION_EVENT_EXPIRE_AFTER_ID_DIFFERENCE
from .fields import (
    parse_application_id, parse_application_permissions, parse_authorizer_user_ids, parse_channel, parse_entitlements,
    parse_guild, parse_id, parse_message, parse_token, parse_type, parse_user, parse_user_locale,
    parse_user_permissions, put_application_id_into, put_application_permissions_into, put_authorizer_user_ids_into,
    put_channel_into, put_entitlements_into, put_guild_into, put_id_into, put_message_into, put_token_into,
    put_type_into, put_user_into, put_user_locale_into, put_user_permissions_into, validate_application_id,
    validate_application_permissions, validate_authorizer_user_ids, validate_channel, validate_entitlements,
    validate_guild, validate_id, validate_interaction, validate_message, validate_token, validate_type, validate_user,
    validate_user_locale, validate_user_permissions
)
from .preinstanced import InteractionType


create_partial_guild_from_id = include('create_partial_guild_from_id')



PRECREATE_FIELDS = {
    'application': ('application_id', validate_application_id),
    'application_id': ('application_id', validate_application_id),
    'application_permissions': ('application_permissions', validate_application_permissions),
    'authorizer_user_ids': ('authorizer_user_ids', validate_authorizer_user_ids),
    'channel': ('channel', validate_channel),
    'entitlements': ('entitlements', validate_entitlements),
    'guild': ('guild', validate_guild),
    'user_locale': ('user_locale', validate_user_locale),
    'message': ('message', validate_message),
    'token': ('token', validate_token),
    'user': ('user', validate_user),
    'user_permissions': ('user_permissions', validate_user_permissions),
}


@export
class InteractionEvent(DiscordEntity, EventBase, immortal = True):
    """
    Represents a processed `INTERACTION_CREATE` dispatch event.
    
    Attributes
    ----------
    id : `int`
        The interaction's id.
    
    _async_task : `None`, ``Task``
        Task set if interaction event is acknowledged asynchronously.
    
    _response_flags : `int`
        The response order state of ``InteractionEvent``
        
        +-------------------------------+-------+---------------------------------------------------+
        | Respective name               | Shift | Description                                       |
        +===============================+=======+===================================================+
        | RESPONSE_FLAG_DEFERRING       | 0     | The vent is being acknowledged.                   |
        +-------------------------------+-------+---------------------------------------------------+
        | RESPONSE_FLAG_DEFERRED        | 1     | The event was acknowledged and response will be   |
        |                               |       | sent later. Shows loading screen for the user.    |
        +-------------------------------+-------+---------------------------------------------------+
        | RESPONSE_FLAG_RESPONDING      | 2     | Responding to the interaction.                    |
        +-------------------------------+-------+---------------------------------------------------+
        | RESPONSE_FLAG_RESPONDED       | 3     | Response was sent on the interaction.             |
        +-------------------------------+-------+---------------------------------------------------+
        | RESPONSE_FLAG_EPHEMERAL       | 4     | Whether the main response is an ephemeral,        |
        |                               |       | showing for the invoking user only.               |
        +-------------------------------+-------+---------------------------------------------------+
        
        Can be used by extensions and is used by the the ``Client``-s to ensure correct flow order.
    
    application_id : `int`
        The interaction's application's identifier.
    
    application_permissions : ``Permission``
        The permissions granted to the application in the guild.
    
    authorizer_user_ids : `None | dict<ApplicationIntegrationType, int>`
        The users' identifier who authorized the integration.
    
    entitlements : `None`, `tuple` of ``Entitlement``
        The applicable entitlements for the event's context.
        These can both target guild and user as well.
    
    channel : ``Channel``
        The channel from where the interaction was called.
    
    guild : `None`, ``Guild``
        The guild from where the interaction was called from.
    
    interaction : ``InteractionMetadataBase``
        Contain additional details of the interaction.
    
    message : `None`, ``Message``
        The message from where the interaction was received. Applicable for message components.
    
    token : `str`
        Interaction's token used when responding on it.
    
    type : ``InteractionType``
        The interaction's type.
    
    user : ``ClientUserBase``
        The user who called the interaction.
    
    user_locale : ``Locale``
        The selected language of the invoking user.
    
    user_permissions : ``Permission``
        The user's permissions in the respective channel.
    
    Notes
    -----
    The interaction token can be used for 15 minutes, tho if it is not used within the first 3 seconds, it is
    invalidated immediately.
    
    Interaction event instances are weakreferable.
    """
    __slots__ = (
        '_async_task', '_response_flags', 'application_id', 'application_permissions', 'authorizer_user_ids',
        'entitlements', 'channel', 'guild', 'interaction', 'message', 'token', 'type', 'user', 'user_locale',
        'user_permissions'
    )
    
    def __new__(
        cls,
        *,
        application_id = ...,
        application_permissions = ...,
        authorizer_user_ids = ...,
        channel = ...,
        entitlements = ...,
        guild = ...,
        guild_locale = ...,
        interaction = ...,
        interaction_type = ...,
        locale = ...,
        message = ...,
        token = ..., 
        user = ...,
        user_locale = ...,
        user_permissions = ...,
    ):
        """
        Creates a partial interaction event.
        
        Parameters
        ----------
        application_id : `int`, `str`, Optional (Keyword only)
            The interaction's application's identifier.
        
        application_permissions : ``Permission``, `int`, Optional (Keyword only)
            The permissions granted to the application in the guild.
        
        authorizer_user_ids : `None | dict<ApplicationIntegrationType | int, int | ClientUserBase>` \
                , Optional (Keyword only)
            The users' identifier who authorized the integration.
        
        channel : ``Channel``, Optional (Keyword only)
            The channel from where the interaction was called.
        
        entitlements : `None`, `iterable` of ``Entitlement``, Optional (Keyword only)
            The applicable entitlements for the event's context.
        
        guild : `None`, ``Guild``, Optional (Keyword only)
            The guild from where the interaction was called from.
        
        interaction : ``InteractionMetadataBase``, Optional (Keyword only)
            Contain additional details of the interaction.
        
        message : `None`, ``Message``, Optional (Keyword only)
            The message from where the interaction was received.
        
        token : `str`, Optional (Keyword only)
            Interaction's token used when responding on it.
        
        type : ``InteractionType``, `int`, Optional (Keyword only)
            The interaction's type.
        
        user : ``ClientUserBase``, Optional (Keyword only)
            The user who called the interaction.
        
        user_locale : ``Locale``, `str`, Optional (Keyword only)
            The selected language of the invoking user.
        
        user_permissions : ``Permission``, `int`, Optional (Keyword only)
            The user's permissions in the respective channel.
        
        Returns
        -------
        self : `instance<cls>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's type is incorrect.
        """
        # application_id
        if application_id is ...:
            application_id = 0
        else:
            application_id = validate_application_id(application_id)
        
        # application_permissions
        if application_permissions is ...:
            application_permissions = Permission()
        else:
            application_permissions = validate_application_permissions(application_permissions)
        
        # authorizer_user_ids
        if authorizer_user_ids is ...:
            authorizer_user_ids = None
        else:
            authorizer_user_ids = validate_authorizer_user_ids(authorizer_user_ids)
        
        # channel
        if channel is ...:
            channel = create_partial_channel_from_id(0, ChannelType.unknown, 0)
        else:
            channel = validate_channel(channel)
        
        # entitlements
        if entitlements is ...:
            entitlements = None
        else:
            entitlements = validate_entitlements(entitlements)
        
        # guild
        if guild is ...:
            guild = None
        else:
            guild = validate_guild(guild)
        
        # interaction & interaction_type
        if interaction_type is ...:
            interaction_type = InteractionType.none
        else:
            interaction_type = validate_type(interaction_type)
        
        if interaction is ...:
            interaction = interaction_type.metadata_type()
        else:
            interaction = validate_interaction(interaction, interaction_type)
        
        # message
        if message is ...:
            message = None
        else:
            message = validate_message(message)
        
        # token
        if token is ...:
            token = ''
        else:
            token = validate_token(token)
        
        # user
        if user is ...:
            user = ZEROUSER
        else:
            user = validate_user(user)
        
        # user_locale
        if user_locale is ...:
            user_locale = LOCALE_DEFAULT
        else:
            user_locale = validate_user_locale(user_locale)
        
        # user_permissions
        if user_permissions is ...:
            user_permissions = Permission()
        else:
            user_permissions = validate_user_permissions(user_permissions)
        
        # Construct
        
        self = object.__new__(cls)
        self._async_task = None
        self._response_flags = RESPONSE_FLAG_NONE
        self.id = 0
        self.application_id = application_id
        self.application_permissions = application_permissions
        self.authorizer_user_ids = authorizer_user_ids
        self.channel = channel
        self.entitlements = entitlements
        self.guild = guild
        self.interaction = interaction
        self.message = message
        self.token = token
        self.type = interaction_type
        self.user = user
        self.user_locale = user_locale
        self.user_permissions = user_permissions
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new ``InteractionEvent`` with the given parameters.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            `INTERACTION_CREATE` dispatch event data.
        
        Returns
        -------
        self : `instance<cls>`
        """
        # Need guild_id early, so we can create a guild if required.
        guild = parse_guild(data)
        
        # interaction_id
        interaction_id = parse_id(data)
        application_id = parse_application_id(data)
        application_permissions = parse_application_permissions(data)
        authorizer_user_ids = parse_authorizer_user_ids(data)
        channel = parse_channel(data)
        entitlements = parse_entitlements(data)
        interaction_type = parse_type(data)
        interaction = interaction_type.metadata_type.from_data(data['data'], 0 if guild is None else guild.id)
        user_locale = parse_user_locale(data)
        message = parse_message(data)
        token = parse_token(data)
        user = parse_user(data, 0 if guild is None else guild.id)
        user_permissions = parse_user_permissions(data)
        
        self = object.__new__(cls)
        self._async_task = None
        self._response_flags = RESPONSE_FLAG_NONE
        self.application_id = application_id
        self.application_permissions = application_permissions
        self.authorizer_user_ids = authorizer_user_ids
        self.channel = channel
        self.entitlements = entitlements
        self.guild = guild
        self.interaction = interaction
        self.id = interaction_id
        self.message = message
        self.token = token
        self.type = interaction_type
        self.user = user
        self.user_locale = user_locale
        self.user_permissions = user_permissions
        
        if message is None:
            self._add_response_waiter()
        
        return self
    
    
    def to_data(self, *, defaults = False):
        """
        Returns the interaction event's json serializable representation.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether fields with their default values should be included as well.
        
        Returns
        -------
        data : `dict` of (`str`, `object`) items
        """
        data = {}
        put_application_id_into(self.application_id, data, defaults)
        put_application_permissions_into(self.application_permissions, data, defaults)
        put_authorizer_user_ids_into(self.authorizer_user_ids, data, defaults)
        put_channel_into(self.channel, data, defaults)
        put_entitlements_into(self.entitlements, data, defaults)
        put_guild_into(self.guild, data, defaults)
        put_id_into(self.id, data, defaults)
        put_message_into(self.message, data, defaults)
        put_token_into(self.token, data, defaults)
        put_type_into(self.type, data, defaults)
        put_user_into(self.user, data, defaults, guild_id = self.guild_id)
        put_user_locale_into(self.user_locale, data, defaults)
        put_user_permissions_into(self.user_permissions, data, defaults)
        data['data'] = self.interaction.to_data(defaults = defaults, guild_id = self.guild_id)
        return data
    
    
    @classmethod
    def _create_empty(cls, interaction_id):
        """
        Creates a new partial interaction event with it's attributes set as their default value.
        
        Parameters
        ----------
        interaction_id : `int`
            The interaction event's identifier.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self._async_task = None
        self._response_flags = RESPONSE_FLAG_NONE
        self.application_id = 0
        self.application_permissions = Permission()
        self.authorizer_user_ids = None
        self.channel = create_partial_channel_from_id(0, ChannelType.unknown, 0)
        self.entitlements = None
        self.guild = None
        self.id = interaction_id
        self.interaction = DEFAULT_INTERACTION_METADATA
        self.token = ''
        self.type = InteractionType.none
        self.user = ZEROUSER
        self.user_locale = LOCALE_DEFAULT
        self.user_permissions = Permission()
        self.message = None
        return self
    
    
    @classmethod
    def precreate(
        cls,
        interaction_id,
        **keyword_parameters,
    ):
        """
        Creates an interaction event. Not like ``.__new__``, ``.precreate`` allows setting ``.id`` as well.
        
        Since interaction events are not cached, there os no major advantage of using this method.
        
        Parameters
        ----------
        interaction_id : `int`
            The interaction's identifier.
        
        **keyword_parameters : Keyword parameters
            Additional keyword parameters defining which attribute and how should be set.
        
        Other Parameters
        ----------
        application : `int`, `str`, ``Application``, Optional (Keyword only)
            Alternative for `application_id`.
        
        application_id : `int`, `str`, ``Application``, Optional (Keyword only)
            The interaction's application's identifier.
        
        application_permissions : ``Permission``, `int`, Optional (Keyword only)
            The permissions granted to the application in the guild.
        
        authorizer_user_ids : `None | dict<ApplicationIntegrationType | int, int | ClientUserBase>` \
                , Optional (Keyword only)
            The users' identifier who authorized the integration.
        
        channel : ``Channel``, Optional (Keyword only)
            The channel from where the interaction was called.
        
        entitlements : `None`, `iterable` of ``Entitlement``, Optional (Keyword only)
            The applicable entitlements for the event's context.
        
        guild : `None`, ``Guild``, Optional (Keyword only)
            The guild from where the interaction was called from.
        
        interaction : ``InteractionMetadataBase``, Optional (Keyword only)
            Contain additional details of the interaction.
        
        interaction_type : ``InteractionType``, `int`, Optional (Keyword only)
            The interaction's type.
        
        message : `None`, ``Message``, Optional (Keyword only)
            The message from where the interaction was received.
        
        token : `str`, Optional (Keyword only)
            Interaction's token used when responding on it.
        
        user : ``ClientUserBase``, Optional (Keyword only)
            The user who called the interaction.
        
        user_locale : ``Locale``, `str`, Optional (Keyword only)
            The selected language of the invoking user.
        
        user_permissions : ``Permission``, `int`, Optional (Keyword only)
            The user's permissions in the respective channel.
            
        Returns
        -------
        self : `instance<cls>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's type is incorrect.
        """
        interaction_id = validate_id(interaction_id)
        
        if keyword_parameters:
            processed = []
            
            # interaction & interaction_type
            try:
                interaction_type = keyword_parameters.pop('interaction_type')
            except KeyError:
                interaction_type = InteractionType.none
            else:
                interaction_type = validate_type(interaction_type)
                processed.append(('type', interaction_type))
            
            try:
                interaction = keyword_parameters.pop('interaction')
            except KeyError:
                if interaction_type is not InteractionType.none:
                    interaction = interaction_type.metadata_type()
                    processed.append(('interaction', interaction))
            else:
                interaction = validate_interaction(interaction, interaction_type)
                processed.append(('interaction', interaction))
            
            
            extra = process_precreate_parameters(keyword_parameters, PRECREATE_FIELDS, processed)
            raise_extra(extra)
        
        else:
            processed = None
        
        self = cls._create_empty(interaction_id)
        
        if (processed is not None):
            for item in processed:
                setattr(self, *item)
        
        return self
    
    
    def copy(self):
        """
        Copies the interaction event.
        The returned interaction event is partial lacking internal fields.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new._async_task = None
        new._response_flags = RESPONSE_FLAG_NONE
        new.id = 0
        new.application_id = self.application_id
        new.application_permissions = self.application_permissions
        
        authorizer_user_ids = self.authorizer_user_ids
        if (authorizer_user_ids is not None):
            authorizer_user_ids = authorizer_user_ids.copy()
        new.authorizer_user_ids = authorizer_user_ids
        
        new.type = self.type
        new.channel = self.channel
        
        entitlements = self.entitlements
        if (entitlements is not None):
            entitlements = (*entitlements,)
        new.entitlements = entitlements
        
        new.guild = self.guild
        new.interaction = self.interaction.copy()
        new.token = self.token
        new.user = self.user
        new.user_locale = self.user_locale
        new.user_permissions = self.user_permissions
        new.message = self.message
        return new
    
    
    def copy_with(
        self,
        *,
        application_id = ...,
        application_permissions = ...,
        authorizer_user_ids = ...,
        channel = ...,
        entitlements = ...,
        guild = ...,
        interaction = ...,
        interaction_type = ...,
        message = ...,
        token = ..., 
        user = ...,
        user_locale = ...,
        user_permissions = ...,
    ):
        """
        Copies the interaction event modifying it's defined fields.
        The returned interaction event is partial lacking internal fields.
        
        Parameters
        ----------
        application_id : `int`, `str`, Optional (Keyword only)
            The interaction's application's identifier.
        
        application_permissions : ``Permission``, `int`, Optional (Keyword only)
            The permissions granted to the application in the guild.
        
        authorizer_user_ids : `None | dict<ApplicationIntegrationType | int, int | ClientUserBase>` \
                , Optional (Keyword only)
            The users' identifier who authorized the integration.
        
        channel : ``Channel``, Optional (Keyword only)
            The channel from where the interaction was called.
        
        channel_id : `int`, `str`, ``Channel``, Optional (Keyword only)
            The channel's identifier from where the interaction was called.
        
        entitlements : `None`, `iterable` of ``Entitlement``, Optional (Keyword only)
            The applicable entitlements for the event's context.
        
        guild : `None`, ``Guild```, Optional (Keyword only)
            The guild from where the interaction was called from.
        
        interaction : ``InteractionMetadataBase``, Optional (Keyword only)
            Contain additional details of the interaction.
        
        message : `None`, ``Message``, Optional (Keyword only)
            The message from where the interaction was received.
        
        token : `str`, Optional (Keyword only)
            Interaction's token used when responding on it.
        
        type : ``InteractionType``, `int`, Optional (Keyword only)
            The interaction's type.
        
        user : ``ClientUserBase``, Optional (Keyword only)
            The user who called the interaction.
        
        user_locale : ``Locale``, `str`, Optional (Keyword only)
            The selected language of the invoking user.
        
        user_permissions : ``Permission``, `int`, Optional (Keyword only)
            The user's permissions in the respective channel.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's type is incorrect.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        # application_id
        if application_id is ...:
            application_id = self.application_id
        else:
            application_id = validate_application_id(application_id)
        
        # application_permissions
        if application_permissions is ...:
            application_permissions = self.application_permissions
        else:
            application_permissions = validate_application_permissions(application_permissions)
        
        # authorizer_user_ids
        if authorizer_user_ids is ...:
            authorizer_user_ids = self.authorizer_user_ids
            if (authorizer_user_ids is not None):
                authorizer_user_ids = authorizer_user_ids.copy()
        
        else:
            authorizer_user_ids = validate_authorizer_user_ids(authorizer_user_ids)
        
        # guild
        if guild is ...:
            guild = self.guild
        else:
            guild = validate_guild(guild)
        
        # channel
        if channel is ...:
            channel = self.channel
        else:
            channel = validate_channel(channel)
        
        # entitlements
        if entitlements is ...:
            entitlements = self.entitlements
            if (entitlements is not None):
                entitlements = (*entitlements,)
        else:
            entitlements = validate_entitlements(entitlements)
        
        # interaction & interaction_type
        if interaction_type is ...:
            interaction_type = self.type
        else:
            interaction_type = validate_type(interaction_type)
        
        if interaction is ...:
            if interaction_type is self.type:
                interaction = self.interaction.copy()
            else:
                interaction = interaction_type.metadata_type()
        else:
            interaction = validate_interaction(interaction, interaction_type)
        
        # message
        if message is ...:
            message = self.message
        else:
            message = validate_message(message)
        
        # token
        if token is ...:
            token = self.token
        else:
            token = validate_token(token)
        
        # user
        if user is ...:
            user = self.user
        else:
            user = validate_user(user)
        
        # user_locale
        if user_locale is ...:
            user_locale = self.user_locale
        else:
            user_locale = validate_user_locale(user_locale)
        
        # user_permissions
        if user_permissions is ...:
            user_permissions = self.user_permissions
        else:
            user_permissions = validate_user_permissions(user_permissions)
        
        # Construct
        new = object.__new__(type(self))
        new._async_task = None
        new._response_flags = RESPONSE_FLAG_NONE
        new.id = 0
        new.application_id = application_id
        new.application_permissions = application_permissions
        new.authorizer_user_ids = authorizer_user_ids
        new.type = interaction_type
        new.channel = channel
        new.entitlements = entitlements
        new.guild = guild
        new.interaction = interaction
        new.token = token
        new.user = user
        new.user_locale = user_locale
        new.user_permissions = user_permissions
        new.message = message
        
        return new
    
    
    async def wait_for_response_message(self, *, timeout = None):
        """
        Waits for response message. Applicable for application command interactions.
        
        This method is a coroutine.
        
        Parameters
        ----------
        timeout : `None`, `float` = `None`, Optional (Keyword only)
            The maximal time to wait for message before `TimeoutError` is raised.
        
        Returns
        -------
        message : ``Message``
            The received message.
        
        Raises
        ------
        TimeoutError
            Message was not received before timeout.
        """
        message = self.message
        if (message is not None):
            return message
        
        try:
            waiter = INTERACTION_EVENT_MESSAGE_WAITERS[self]
        except KeyError:
            waiter = Future(KOKORO)
            INTERACTION_EVENT_MESSAGE_WAITERS[self] = waiter
        
        waiter = shield(waiter, KOKORO)
        
        if (timeout is not None):
            waiter.apply_timeout(timeout)
        
        await waiter
        return self.message
    
    
    def __repr__(self):
        """Returns the representation of the event."""
        repr_parts = ['<', self.__class__.__name__]
        
        response_state_names = None
        response_state = self._response_flags
        
        if response_state == RESPONSE_FLAG_NONE:
            pass
        
        if response_state & RESPONSE_FLAG_DEFERRING:
            if response_state_names is None:
                response_state_names = []
            response_state_names.append('deferring')
        
        if response_state & RESPONSE_FLAG_DEFERRED:
            if response_state_names is None:
                response_state_names = []
            response_state_names.append('deferred')
        
        if response_state & RESPONSE_FLAG_RESPONDING:
            if response_state_names is None:
                response_state_names = []
            response_state_names.append('responding')
        
        if response_state & RESPONSE_FLAG_RESPONDED:
            if response_state_names is None:
                response_state_names = []
            response_state_names.append('responded')
        
        if response_state & RESPONSE_FLAG_EPHEMERAL:
            if response_state_names is None:
                response_state_names = []
            response_state_names.append('ephemeral')
        
        if (response_state_names is not None):
            repr_parts.append(' (')
            index = 0
            limit = len(response_state_names)
            while True:
                response_state_name = response_state_names[index]
                repr_parts.append(response_state_name)
                index += 1
                if index == limit:
                    break
                
                repr_parts.append(', ')
                continue
            
            repr_parts.append('),')
        
        repr_parts.append(' type = ')
        metadata_type = self.type
        repr_parts.append(metadata_type.name)
        repr_parts.append(' ~ ')
        repr_parts.append(repr(metadata_type.value))
        
        authorizer_user_ids = self.authorizer_user_ids
        if (authorizer_user_ids is not None):
            repr_parts.append(', authorizer_user_ids = ')
            repr_parts.append(repr(authorizer_user_ids))
        
        guild = self.guild
        if guild is not None:
            repr_parts.append(', guild_id = ')
            repr_parts.append(repr(guild.id))
            
            repr_parts.append(', application_permissions = ')
            repr_parts.append(format(self.application_permissions, 'd'))
        
        
        repr_parts.append(', channel = ')
        repr_parts.append(repr(self.channel))
        
        # entitlements
        entitlements = self.entitlements
        if (entitlements is not None):
            length = len(entitlements)
            index = 0
            
            repr_parts.append(', entitlements = [')
            while True:
                entitlement = entitlements[index]
                index += 1
                
                repr_parts.append(repr(entitlement))
                
                if index == length:
                    break
                
                repr_parts.append(', ')
                continue
            
            repr_parts.append(']' )
        
        
        message = self.message
        if (message is not None):
            repr_parts.append(', message = ')
            repr_parts.append(repr(message))
        
        
        repr_parts.append(', user = ')
        repr_parts.append(repr(self.user))
        
        repr_parts.append(', user_locale = ')
        repr_parts.append(repr(self.user_locale.name))
        
        if guild is not None:
            repr_parts.append(', guild_locale = ')
            repr_parts.append(repr(guild.locale.name))
        
        repr_parts.append(', interaction = ')
        repr_parts.append(repr(self.interaction))
        
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two interaction events are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        # Shortcut
        if self is other:
            return True
        
        # id
        self_id = self.id
        other_id = other.id
        if self_id and other_id and (self.id != other.id):
            return False
        
        # application_id
        if self.application_id != other.application_id:
            return False
        
        # application_permissions
        if self.application_permissions != other.application_permissions:
            return False
        
        # authorizer_user_ids
        if self.authorizer_user_ids != other.authorizer_user_ids:
            return False
        
        # channel
        if self.channel is not other.channel:
            return False
        
        # entitlements
        if self.entitlements != other.entitlements:
            return False
        
        # guild
        if self.guild is not other.guild:
            return False
        
        # interaction
        if self.interaction != other.interaction:
            return False
        
        # message
        if self.message is not other.message:
            return False
        
        # token
        if self.token != other.token:
            return False
        
        # type
        if self.type is not other.type:
            return False
        
        # user
        if self.user is not other.user:
            return False
        
        # user_locale
        if self.user_locale is not other.user_locale:
            return False
        
        # user_permissions
        if self.user_permissions != other.user_permissions:
            return False
        
        return True
    
    
    def __hash__(self):
        """Returns the hash value of the interaction event."""
        self_id = self.id
        if self_id:
            return self_id
        
        hash_value = 0
        
        # application_id
        hash_value ^= self.application_id
        
        # application_permissions
        hash_value ^= self.application_permissions
        
        # authorizer_user_ids
        authorizer_user_ids = self.authorizer_user_ids
        if (authorizer_user_ids is not None):
            hash_value ^= len(authorizer_user_ids) << 8
            for integration_type, user_id in authorizer_user_ids.items():
                hash_value ^= (integration_type.value << 22) & user_id
        
        # channel
        hash_value ^= hash(self.channel)
        
        # entitlements
        entitlements = self.entitlements
        if (entitlements is not None):
            hash_value ^= hash(entitlements)
        
        # guild
        guild = self.guild
        if (guild is not None):
            hash_value ^= hash(guild)
        
        # interaction
        hash_value ^= hash(self.interaction)
        
        # message
        message = self.message
        if (message is not None):
            hash_value ^= hash(self.message)
        
        # token
        hash_value ^= hash(self.token)
        
        # type
        hash_value ^= self.type.value
        
        # user
        hash_value ^= hash(self.user)
        
        # user_locale
        hash_value ^= hash(self.user_locale)
        
        # user_permissions
        hash_value ^= self.user_permissions
        
        return hash_value
    
    
    def is_unanswered(self):
        """
        Returns whether the event was not acknowledged and not acknowledging either.
        
        Returns
        -------
        is_unanswered : `bool`
        """
        return True if (self._response_flags == RESPONSE_FLAG_NONE) else False
    
    
    def is_acknowledging(self):
        """
        Returns whether the event is being acknowledged.
        
        Returns
        -------
        is_acknowledging : `bool`
        """
        return True if (self._response_flags & RESPONSE_FLAG_ACKNOWLEDGING) else False
    
    
    def is_acknowledged(self):
        """
        Returns whether the event is acknowledged.
        
        Returns
        -------
        is_acknowledged : `bool`
        """
        return True if (self._response_flags & RESPONSE_FLAG_ACKNOWLEDGED) else False
    
    
    def is_deferred(self):
        """
        Returns whether the event is deferred.
        
        Returns
        -------
        is_deferred : `bool`
        """
        response_state = self._response_flags
        if response_state & RESPONSE_FLAG_RESPONDED:
            return False
        
        if response_state & RESPONSE_FLAG_DEFERRED:
            return True
        
        return False
    
    
    def is_responding(self):
        """
        Returns whether the event it being responded.
        
        Returns
        -------
        is_responding : `bool`
        """
        return True if (self._response_flags & RESPONSE_FLAG_RESPONDING) else False
    
    
    def is_responded(self):
        """
        Returns whether was responded.
        
        Returns
        -------
        is_responded : `bool`
        """
        return True if (self._response_flags & RESPONSE_FLAG_RESPONDED) else False
    
    
    def is_expired(self):
        """
        Returns whether the event is already expired.
        
        Returns
        -------
        is_expired : `bool`
        """
        return now_as_id() > (self.id + INTERACTION_EVENT_EXPIRE_AFTER_ID_DIFFERENCE)
    
    
    def __len__(self):
        """Helper for unpacking if needed."""
        return 3
    
    
    def __iter__(self):
        """
        Unpacks the event.
        
        This method is a generator.
        """
        yield self.type
        yield self.user
        yield self.interaction
    
    
    @property
    def channel_id(self):
        """
        Returns the interaction's channel's identifier.
        
        Returns
        -------
        channel_id : `int`
        """
        return self.channel.id
    
    
    @property
    def user_id(self):
        """
        Returns the interaction's user's identifier.
        
        Returns
        -------
        user_id : `int`
        """
        return self.user.id
    
    
    @property
    def guild_id(self):
        """
        Returns the interaction's guild's identifier.
        
        Returns
        -------
        guild_id : ``int`
        """
        guild = self.guild
        if guild is None:
            guild_id = 0
        else:
            guild_id = guild.id
        
        return guild_id
    
    
    @property
    def guild_locale(self):
        """
        Returns the interaction's guild's locale.
        
        Returns
        -------
        guild_locale : ``Locale``
        """
        guild = self.guild
        if guild is None:
            guild_locale = LOCALE_DEFAULT
        else:
            guild_locale = guild.locale
        
        return guild_locale
    
    
    @property
    def client(self):
        """
        Returns the interaction's client.
        
        Returns
        -------
        client : `Client`
        
        Raises
        ------
        RuntimeError
            Client could not be identified.
        """
        try:
            return APPLICATION_ID_TO_CLIENT[self.application_id]
        except KeyError:
            raise RuntimeError(
                f'Client of {self!r} could not be identified.'
            ) from None
    
    
    @property
    def voice_client(self):
        """
        Returns the voice client of the interaction's client in it's guild.
        
        Returns
        -------
        voice_client : `None`, ``VoiceClient``
        """
        try:
            client = APPLICATION_ID_TO_CLIENT[self.application_id]
        except KeyError:
            voice_client = None
        else:
            guild = self.guild
            if guild is None:
                voice_client = None
            else:
                voice_client = client.voice_clients.get(guild.id, None)
        
        return voice_client
    
    
    def has_entitlement(self, entitlement):
        """
        Returns whether the interaction event hast he given entitlement.
        
        Parameters
        ----------
        entitlement : ``Entitlement``
            The entitlement to look for.
        
        Returns
        -------
        has_entitlement : `bool`
        """
        entitlements = self.entitlements
        if entitlements is None:
            return False
        
        return entitlement in entitlements
    
    
    def iter_entitlements(self):
        """
        Iterates over the entitlements of the interaction event.
        
        This method is an iterable generator.
        
        Yields
        ------
        entitlement : ``Entitlement``
        """
        entitlements = self.entitlements
        if (entitlements is not None):
            yield from entitlements
    
    
    def has_sku(self, sku):
        """
        Returns whether any of the interaction event's entitlements grants access to the given stock keeping unit.
        
        Parameters
        ----------
        sku : ``SKU``
            Stock keeping unit to look for.
        
        Returns
        -------
        has_sku : `bool`
        """
        entitlements = self.entitlements
        if (entitlements is None):
            return False
        
        sku_id = sku.id
        
        for entitlement in entitlements:
            if entitlement.sku_id == sku_id:
                return True
        
        return False
    
    
    def _add_response_waiter(self):
        """
        Adds the interaction event to response waiters.
        
        Called when the interaction is application command one, to resolve it's ``.message`` attribute when created.
        """
        INTERACTION_EVENT_RESPONSE_WAITERS[self.id] = self
    
    
    async def _wait_for_async_task_completion(self):
        """
        Waits for async task's completion.
        
        This method is a coroutine.
        """
        async_task = self._async_task
        if (async_task is not None) and (async_task is not KOKORO.current_task):
            try:
                await async_task
            finally:
                self._async_task = None
    
    
    # Field Proxies
    
    @property
    @copy_docs(InteractionMetadataBase.component_type)
    def component_type(self):
        return self.interaction.component_type
    
    
    @property
    @copy_docs(InteractionMetadataBase.components)
    def components(self):
        return self.interaction.components
    
    
    @property
    @copy_docs(InteractionMetadataBase.custom_id)
    def custom_id(self):
        return self.interaction.custom_id
    
    
    @property
    @copy_docs(InteractionMetadataBase.id)
    def application_command_id(self):
        return self.interaction.id
    
    
    @property
    @copy_docs(InteractionMetadataBase.name)
    def application_command_name(self):
        return self.interaction.name
    
    
    @property
    @copy_docs(InteractionMetadataBase.options)
    def options(self):
        return self.interaction.options
    
    
    @property
    @copy_docs(InteractionMetadataBase.resolved)
    def resolved(self):
        return self.interaction.resolved
    
    
    @property
    @copy_docs(InteractionMetadataBase.target_id)
    def target_id(self):
        return self.interaction.target_id
    
    
    @property
    @copy_docs(InteractionMetadataBase.values)
    def values(self):
        return self.interaction.values
    
    # application command
    
    @property
    @copy_docs(InteractionMetadataBase.target)
    def target(self):
        return self.interaction.target
    
    # application command autocomplete
    
    @copy_docs(InteractionMetadataBase.iter_options)
    def iter_options(self):
        return (yield from self.interaction.iter_options())
    
    
    @property
    @copy_docs(InteractionMetadataBase.focused_option)
    def focused_option(self):
        return self.interaction.focused_option
    
    
    @copy_docs(InteractionMetadataBase.get_non_focused_values)
    def get_non_focused_values(self):
        return self.interaction.get_non_focused_values()
    
    
    @copy_docs(InteractionMetadataBase.get_value_of)
    def get_value_of(self, *option_names):
        return self.interaction.get_value_of(*option_names)
    
    
    @property
    @copy_docs(InteractionMetadataBase.value)
    def value(self):
        return self.interaction.value
    
    # Message component
    
    @copy_docs(InteractionMetadataBase.iter_values)
    def iter_values(self):
        return (yield from self.interaction.iter_values())
    
    
    @copy_docs(InteractionMetadataBase.iter_entities)
    def iter_entities(self):
        return (yield from self.interaction.iter_entities())
    
    
    @property
    @copy_docs(InteractionMetadataBase.entities)
    def entities(self):
        return self.interaction.entities
    
    # form submit
    
    @copy_docs(InteractionMetadataBase.iter_components)
    def iter_components(self):
        return (yield from self.interaction.iter_components())
    
    
    @copy_docs(InteractionMetadataBase.iter_custom_ids_and_values)
    def iter_custom_ids_and_values(self):
        return (yield from self.interaction.iter_custom_ids_and_values())
    
    
    @copy_docs(InteractionMetadataBase.get_custom_id_value_relation)
    def get_custom_id_value_relation(self):
        return self.interaction.get_custom_id_value_relation()
    
    
    @copy_docs(InteractionMetadataBase.get_value_for)
    def get_value_for(self, custom_id_to_match):
        return self.interaction.get_value_for(custom_id_to_match)
    
    
    @copy_docs(InteractionMetadataBase.get_match_and_value)
    def get_match_and_value(self, matcher):
        return self.interaction.get_match_and_value(matcher)
    
    
    @copy_docs(InteractionMetadataBase.iter_matches_and_values)
    def iter_matches_and_values(self, matcher):
        return (yield from self.interaction.iter_matches_and_values(matcher))
    
    # resolved
    
    @copy_docs(InteractionMetadataBase.resolve_attachment)
    def resolve_attachment(self, attachment_id):
        return self.interaction.resolve_attachment(attachment_id)
    
    
    @copy_docs(InteractionMetadataBase.resolve_channel)
    def resolve_channel(self, channel_id):
        return self.interaction.resolve_channel(channel_id)
    
    
    @copy_docs(InteractionMetadataBase.resolve_message)
    def resolve_message(self, message_id):
        return self.interaction.resolve_message(message_id)
    
    
    @copy_docs(InteractionMetadataBase.resolve_role)
    def resolve_role(self, role_id):
        return self.interaction.resolve_role(role_id)
    
    
    @copy_docs(InteractionMetadataBase.resolve_user)
    def resolve_user(self, user_id):
        return self.interaction.resolve_user(user_id)
    
    
    @copy_docs(InteractionMetadataBase.resolve_mentionable)
    def resolve_mentionable(self, mentionable_id):
        return self.interaction.resolve_mentionable(mentionable_id)
    
    
    @copy_docs(InteractionMetadataBase.resolve_entity)
    def resolve_entity(self, entity_id):
        return self.interaction.resolve_entity(entity_id)
    
    
    # authorized_user_ids
    
    def get_authorizer_user_id(self, integration_type):
        """
        Gets the authorizer user's identifier for the given integration type.
        
        Parameters
        ----------
        integration_type : `ApplicationIntegrationType | int`
            Integration type to query for.
        
        Returns
        -------
        user_id : `int`
        """
        authorizer_user_ids = self.authorizer_user_ids
        if (authorizer_user_ids is not None):
            try:
                return authorizer_user_ids[integration_type]
            except KeyError:
                pass
        
        return 0
    
    
    def get_authorizer_user(self, integration_type):
        """
        Gets the authorizer user for the given integration type.
        
        Parameters
        ----------
        integration_type : `ApplicationIntegrationType | int`
            Integration type to query for.
        
        Returns
        -------
        user : `None | ClientUserBase`
        """
        user_id = self.get_authorizer_user_id(integration_type)
        if user_id:
            return create_partial_user_from_id(user_id)
