__all__ = ('Webhook', )

from scarletio import copy_docs, export, include

from ...bases import ICON_TYPE_NONE, Icon
from ...core import USERS
from ...exceptions import DiscordException, ERROR_CODES
from ...http import urls as module_urls
from ...http.urls import WEBHOOK_URL_PATTERN
from ...precreate_helpers import process_precreate_parameters_and_raise_extra
from ...user import ClientUserBase, UserBase, ZEROUSER
from ...user.user.fields import parse_id, put_id_into, put_webhook_name_into, validate_id, validate_webhook_name

from ..webhook_source_channel import WebhookSourceChannel
from ..webhook_source_guild import WebhookSourceGuild

from .fields import (
    parse_application_id, parse_channel_id, parse_source_channel, parse_source_guild, parse_token, parse_type,
    parse_user, put_application_id_into, put_channel_id_into, put_source_channel_into, put_source_guild_into,
    put_token_into, put_type_into, put_user_into, validate_application_id, validate_channel_id,
    validate_source_channel, validate_source_guild, validate_token, validate_type, validate_user
)
from .preinstanced import WebhookType
from .webhook_base import WebhookBase


create_partial_webhook_from_id = include('create_partial_webhook_from_id')


PRECREATE_FIELDS = {
    'application': ('application_id', validate_application_id),
    'application_id': ('application_id', validate_application_id),
    'avatar': ('avatar', UserBase.avatar.validate_icon),
    'channel': ('channel_id', validate_channel_id),
    'channel_id': ('channel_id', validate_channel_id),
    'name': ('name', validate_webhook_name),
    'source_channel': ('source_channel', validate_source_channel),
    'source_guild': ('source_guild', validate_source_guild),
    'token': ('token', validate_token),
    'user': ('user', validate_user),
    'webhook_type': ('type', validate_type),
}


@export
class Webhook(WebhookBase):
    """
    Represents a Discord webhook. At some cases it might be used as webhook's user representation.
    
    Attributes
    ----------
    application_id : `int`
        The application's identifier what created the webhook. Defaults to `0` if not applicable.
    avatar_hash : `int`
        The webhook's avatar's hash in `uint128`.
    avatar_type : ``IconType``
        The webhook's avatar's type.
    channel_id : `int`
        The channel's identifier, where the webhook is going to send it's messages.
    id : `int`
        The webhook's unique identifier number.
    name : str
        The webhook's name.
    source_channel : `None`, ``WebhookSourceChannel``
        Representation of the webhook's source channel. Applicable for ``WebhookType.server`` webhooks.
    source_guild : `None`, ``WebhookSourceGuild``
        Representation of the webhook's source guild. Applicable for ``WebhookType.server`` webhooks.
    token : `str`
        The webhook's token. You need an `id` and a `token` to send webhook message. Defaults to empty string.
    type : ``WebhookType``
        The webhook's type.
    user : ``ClientUserBase``
        The creator of the webhook, or `ZEROUSER` if unknown.
    
    Notes
    -----
    Instances of this class are weakreferable.
    """
    __slots__ = ('application_id', 'source_channel', 'source_guild', 'token', 'user')
    
    def __new__(
        cls,
        *,
        application_id = ...,
        avatar = ...,
        channel_id = ...,
        source_channel = ...,
        source_guild = ...,
        name = ...,
        token = ...,
        user = ...,
        webhook_type = ...,
    ):
        """
        Creates a new partial webhook base with the given fields.
        
        Parameters
        ----------
        application_id : `int`, ``Application``, Optional (Keyword only)
            The application's identifier what created the webhook.
        channel_id : `int`, Optional (Keyword only)
            The channel's identifier, where the webhook is going to send it's messages.
        avatar : `None`, ``Icon``, `str`, `bytes-like`, Optional (Keyword only)
            The user's avatar.
        source_channel : `None`, ``WebhookSourceChannel``, Optional (Keyword only)
            Representation of the webhook's source channel.
        source_guild : `None`, ``WebhookSourceGuild``, Optional (Keyword only)
            Representation of the webhook's source guild.
        name : `str`, Optional (Keyword only)
            The user's name.
        token : `str`, Optional (Keyword only)
            The webhook's token.
        user : ``ClientUserBase``, Optional (Keyword only)
            The creator of the webhook.
        webhook_type : ``WebhookType``, `int`, Optional (Keyword only)
            The webhook's type.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # application_id
        if application_id is ...:
            application_id = 0
        else:
            application_id = validate_application_id(application_id)
        
        # source_channel
        if source_channel is ...:
            source_channel = None
        else:
            source_channel = validate_source_channel(source_channel)
        
        # source_guild
        if source_guild is ...:
            source_guild = None
        else:
            source_guild = validate_source_guild(source_guild)
        
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
        
        # Construct
        self = WebhookBase.__new__(
            cls,
            avatar = avatar,
            channel_id = channel_id,
            name = name,
            webhook_type = webhook_type,
        )
        self.application_id = application_id
        self.source_channel = source_channel
        self.source_guild = source_guild
        self.token = token
        self.user = user
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Tries to get the webhook from the existing ones, then update it. If no webhook was found, creates a new one and
        fills it's attributes from the data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Received webhook data.
        
        Returns
        -------
        self : `instance<cls>`
        """
        webhook_id = parse_id(data)
        try:
            self = USERS[webhook_id]
        except KeyError:
            self = object.__new__(cls)
            USERS[webhook_id] = self
            self.id = webhook_id
            self.token = ''
        
        self._set_attributes(data)
        
        return self
    
    
    def to_webhook_data(self, *, defaults = False, include_internals = False):
        """
        Tries to convert the webhook back to a json serializable dictionary.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default values should be included as well.
        
        include_internals : `bool` = `False`, Optional (Keyword only)
            Whether internal fields should be included as well.
        
        Returns
        -------
        data : `dict` of (`str`, `object`) items
        """
        data = {}
        
        type(self).avatar.put_into(self.avatar, data, defaults, as_data = not include_internals)
        put_channel_id_into(self.channel_id, data, defaults)
        put_webhook_name_into(self.name, data, defaults)
        
        if include_internals:
            put_application_id_into(self.application_id, data, defaults)
            put_id_into(self.id, data, defaults)
            put_source_channel_into(self.source_channel, data, defaults)
            put_source_guild_into(self.source_guild, data, defaults)
            put_token_into(self.token, data, defaults)
            put_type_into(self.type, data, defaults)
            put_user_into(self.user, data, defaults, include_internals = include_internals)
        
        return data
    
    
    @copy_docs(UserBase.copy)
    def copy(self):
        new = WebhookBase.copy(self)
        new.application_id = self.application_id
        new.channel_id = self.channel_id
        source_channel = self.source_channel
        if (source_channel is not None):
            source_channel = source_channel.copy()
        new.source_channel = source_channel
        source_guild = self.source_guild
        if (source_guild is not None):
            source_guild = source_guild.copy()
        new.source_guild = source_guild
        new.token = self.token
        new.user = self.user
        return new
    
    
    def copy_with(
        self,
        *,
        application_id = ...,
        avatar = ...,
        channel_id = ...,
        source_channel = ...,
        source_guild = ...,
        name = ...,
        token = ...,
        user = ...,
        webhook_type = ...,
    ):
        """
        Copies the webhook base with the given fields.
        
        Parameters
        ----------
        application_id : `int`, ``Application``, Optional (Keyword only)
            The application's identifier what created the webhook.
        channel_id : `int`, Optional (Keyword only)
            The channel's identifier, where the webhook is going to send it's messages.
        avatar : `None`, ``Icon``, `str`, `bytes-like`, Optional (Keyword only)
            The user's avatar.
        source_channel : `None`, ``WebhookSourceChannel``, Optional (Keyword only)
            Representation of the webhook's source channel.
        source_guild : `None`, ``WebhookSourceGuild``, Optional (Keyword only)
            Representation of the webhook's source guild.
        name : `str`, Optional (Keyword only)
            The user's name.
        token : `str`, Optional (Keyword only)
            The webhook's token.
        user : ``ClientUserBase``, Optional (Keyword only)
            The creator of the webhook.
        webhook_type : ``WebhookType``, `int`, Optional (Keyword only)
            The webhook's type.
        
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
        # application_id
        if application_id is ...:
            application_id = self.application_id
        else:
            application_id = validate_application_id(application_id)
        
        # source_channel
        if source_channel is ...:
            source_channel = self.source_channel
            if (source_channel is not None):
                source_channel = source_channel.copy()
        else:
            source_channel = validate_source_channel(source_channel)
        
        # source_guild
        if source_guild is ...:
            source_guild = self.source_guild
            if (source_guild is not None):
                source_guild = source_guild.copy()
        else:
            source_guild = validate_source_guild(source_guild)
        
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
        
        # Construct
        new = WebhookBase.copy_with(
            self,
            avatar = avatar,
            channel_id = channel_id,
            name = name,
            webhook_type = webhook_type,
        )
        
        new.application_id = application_id
        new.source_channel = source_channel
        new.source_guild = source_guild
        new.token = token
        new.user = user
        return new
    
    
    @copy_docs(WebhookBase._get_hash_partial)
    def _get_hash_partial(self):
        hash_value = WebhookBase._get_hash_partial(self)
        
        # application_id
        hash_value ^= self.application_id
        
        # source_channel
        source_channel = self.source_channel
        if (source_channel is not None):
            hash_value ^= hash(source_channel)
        
        # source_guild
        source_guild = self.source_guild
        if (source_guild is not None):
            hash_value ^= hash(source_guild)
        
        # token
        hash_value ^= hash(self.token)
        
        # user
        user = self.user
        if (user is not ZEROUSER):
            hash_value ^= hash(user)
        
        return user
    
    
    def _set_attributes(self, data):
        """
        Sets the webhook's attributes from the given data.
        
        Not like ``._update_attributes``, this method also sets the attributes that are not expected to be modified.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Received webhook data.
        """
        self._update_attributes(data)
        
        self.application_id = parse_application_id(data)
        self.source_channel = parse_source_channel(data)
        self.source_guild = parse_source_guild(data)
        
        token = parse_token(data)
        if token:
            self.token = token
        
        self.type = parse_type(data)
        self.user = parse_user(data)
    
    
    @copy_docs(WebhookBase._update_attributes)
    def _update_attributes(self, data):
        WebhookBase._update_attributes(self, data)
        self.channel_id = parse_channel_id(data)
    
    
    @copy_docs(WebhookBase._difference_update_attributes)
    def _difference_update_attributes(self, data):
        old_attributes = WebhookBase._difference_update_attributes(self, data)
        
        channel_id = parse_channel_id(data)
        if channel_id != self.channel_id:
            old_attributes['channel_id'] = self.channel_id
            self.channel_id = channel_id
        
        return old_attributes
    
    
    @copy_docs(UserBase._set_default_attributes)
    def _set_default_attributes(self):
        WebhookBase._set_default_attributes(self)
        
        self.application_id = 0
        self.source_guild = None
        self.source_channel = None
        self.token = ''
        self.user = ZEROUSER
    
    
    @classmethod
    def precreate(cls, webhook_id, **keyword_parameters):
        """
        Precreates the webhook by creating a partial one with the given parameters. When the webhook will be loaded,
        the precreated one will be picked up and will be updated. If an already existing webhook would be precreated,
        it will be updated with the given parameters only if it is a partial one.
        
        Parameters
        ----------
        webhook_id : `int`, `str`
            The webhook's id.
        **keyword_parameters : keyword parameters
            Additional predefined attributes for the webhook.
        
        Other Parameters
        ----------------
        application : `int`, ``Application``, Optional (Keyword only)
            Alternative for `application_id`.
        
        application_id : `int`, ``Application``, Optional (Keyword only)
            The application's identifier what created the webhook.
        
        avatar : `None`, ``Icon``, `str`, Optional (Keyword only)
            The webhook's avatar.
        
        channel : `int`, ``Channel``, Optional (Keyword only)
            Alternative for `channel_id`.
        
        channel_id : `int`, ``Channel``, Optional (Keyword only)
            The channel's identifier, where the webhook is going to send it's messages.
        
        name : `str`, Optional (Keyword only)
            The webhook's name.
        
        source_channel : `None`, ``WebhookSourceChannel``, Optional (Keyword only)
            Representation of the webhook's source channel.
        
        source_guild : `None`, ``WebhookSourceGuild``, Optional (Keyword only)
            Representation of the webhook's source guild.
        
        token : `str`, Optional (Keyword only)
            The webhook's token.
        
        user : ``ClientUserBase``, Optional (Keyword only)
            The creator of the webhook.
        
        webhook_type : ``WebhookType``, `int`, Optional (Keyword only)
            The webhook's type.
        
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
        webhook_id = validate_id(webhook_id)
        
        if keyword_parameters:
            processed = process_precreate_parameters_and_raise_extra(keyword_parameters, PRECREATE_FIELDS)
        else:
            processed = None
        
        try:
            self = USERS[webhook_id]
        except KeyError:
            self = cls._create_empty(webhook_id)
            USERS[webhook_id] = self
        else:
            if not self.partial:
                return self
        
        if (processed is not None):
            for item in processed:
                setattr(self, *item)
        
        return self
    
    
    @classmethod
    def from_url(cls, url):
        """
        Tries to parse the webhook's `id` and `token` from the given `url`. If succeeds, returns a partial webhook.
        If parsing fails, returns `None`.
        
        Parameters
        ----------
        url : `str`
            The url of the webhook.
        
        Returns
        -------
        self : `None`, `instance<cls>`
        """
        result = WEBHOOK_URL_PATTERN.fullmatch(url)
        if result is None:
            return None
        
        webhook_id = int(result.group(1))
        webhook_token = result.group(2)
        
        return create_partial_webhook_from_id(webhook_id, webhook_token)
    
    
    url = property(module_urls.webhook_url)
    
    
    @classmethod
    async def _from_follow_data(cls, data, source_channel, target_channel_id, client):
        """
        Creates the webhook, what executes cross-posts.
        
        This method is ensured after following a channel.
        
        This method is a coroutine.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Received webhook data.
        source_channel : ``Channel``
            The followed channel.
        target_channel_id : `int`
            The target channel's identifier where the webhook messages will be sent.
        client : ``Client``
            The client who created the webhook.
        
        Returns
        -------
        self : `instance<cls>`
        """
        webhook_id = int(data['webhook_id'])
        
        guild = source_channel.guild
        if guild is None:
            try:
                extra_data = await client.http.webhook_get(webhook_id)
            except DiscordException as err:
                if err.code == ERROR_CODES.unknown_webhook:
                    # not lucky
                    name = ''
                    avatar_type = ICON_TYPE_NONE
                    avatar_hash = 0
                else:
                    raise
            
            else:
                name = extra_data['name']
                if name is None:
                    name = ''
                
                avatar_type, avatar_hash = Icon.from_base16_hash(data.get('avatar', None))
            
            source_guild = parse_source_guild(data)
        
        else:
            avatar_hash = guild.icon_hash
            avatar_type = guild.icon_type
            name = f'{guild.name} #{source_channel.name}'
            
            source_guild = WebhookSourceGuild.from_guild(guild)
        
        source_channel = WebhookSourceChannel.from_channel(source_channel)
        
        self = object.__new__(cls)
        self.application_id = 0
        self.avatar_hash = avatar_hash
        self.avatar_type = avatar_type
        self.channel_id = target_channel_id
        self.id = webhook_id
        self.name = name
        self.source_channel = source_channel
        self.source_guild = source_guild
        self.token = ''
        self.type = WebhookType.server
        self.user = client
        
        USERS[webhook_id] = self
        
        return self
