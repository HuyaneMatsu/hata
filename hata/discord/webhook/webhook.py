__all__ = ('Webhook', )

from scarletio import copy_docs, export, include

from ..bases import ICON_TYPE_NONE, Icon, instance_or_id_to_instance
from ..core import USERS
from ..exceptions import DiscordException, ERROR_CODES
from ..http import urls as module_urls
from ..http.urls import WEBHOOK_URL_PATTERN
from ..preconverters import preconvert_preinstanced_type, preconvert_snowflake, preconvert_str
from ..user import ClientUserBase, User, UserBase, ZEROUSER

from .preinstanced import WebhookType
from .webhook_base import WebhookBase
from .webhook_sources import WebhookSourceChannel, WebhookSourceGuild


create_partial_webhook_from_id = include('create_partial_webhook_from_id')
create_partial_channel_from_id = include('create_partial_channel_from_id')
Channel = include('Channel')
Client = include('Client')


@export
class Webhook(WebhookBase):
    """
    Represents a Discord webhook. At some cases it might be used as webhook's user representation.
    
    Attributes
    ----------
    id : `int`
        The webhook's unique identifier number.
    name : str
        The webhook's username.
    discriminator : `int`
        The webhook's discriminator. Given to avoid overlapping names.
    avatar_hash : `int`
        The webhook's avatar's hash in `uint128`.
    avatar_type : ``IconType``
        The webhook's avatar's type.
    banner_color : `None`, ``Color``
        The user's banner color if has any.
    banner_hash : `int`
        The user's banner's hash in `uint128`.
    banner_type : ``IconType``
        The user's banner's type.
    channel_id : `int`
        The channel's identifier, where the webhook is going to send it's messages.
    type : ``WebhookType``
        The webhook's type.
    application_id : `int`
        The application's id what created the webhook. Defaults to `0` if not applicable.
    source_channel : `None`, ``WebhookSourceChannel``
        The webhook's source channel. Applicable for ``WebhookType.server`` webhooks.
    source_guild : `None`, ``WebhookSourceGuild``
        The webhook's source guild. Applicable for ``WebhookType.server`` webhooks.
    token : `str`
        The webhook's token. You need an `id` and a `token` to send webhook message. Defaults to empty string.
    user : ``ClientUserBase``
        The creator of the webhook, or `ZEROUSER` if unknown.
    
    Notes
    -----
    Instances of this class are weakreferable.
    """
    __slots__ = ('application_id', 'source_channel', 'source_guild', 'token', 'user')
    
    def __new__(cls, data):
        """
        Tries to get the webhook from the existing ones, then update it. If no webhook was found, creates a new one and
        fills it's attributes from the data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Received webhook data.
        
        Returns
        -------
        webhook : ``Webhook``
        """
        webhook_id = int(data['id'])
        try:
            self = USERS[webhook_id]
        except KeyError:
            self = object.__new__(cls)
            USERS[webhook_id] = self
            self.id = webhook_id
            self.token = ''
        
        self._set_attributes(data)
        self.type = WebhookType.get(data['type'])
        
        application_id = data.get('application_id', None)
        if application_id is None:
            application_id = 0
        else:
            application_id = int(application_id)
        self.application_id = application_id
        
        source_channel_data = data.get('source_channel', None)
        if source_channel_data is None:
            source_channel = None
        else:
            source_channel = WebhookSourceChannel(source_channel_data)
        self.source_channel = source_channel
        
        source_guild_data = data.get('source_guild', None)
        if source_guild_data is None:
            source_guild = None
        else:
            source_guild = WebhookSourceGuild(source_guild_data)
        self.source_guild = source_guild
        
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
        webhook : `None`, ``Webhook``
        """
        result = WEBHOOK_URL_PATTERN.fullmatch(url)
        if result is None:
            return None
        
        webhook_id = int(result.group(1))
        webhook_token = result.group(2)
        
        return create_partial_webhook_from_id(webhook_id, webhook_token)
    
    
    def _set_attributes(self, data):
        self._update_attributes(data)
        
        self.channel_id = int(data['channel_id'])
        
        token = data.get('token', None)
        if (token is not None):
            self.token = token
        
        try:
            user_data = data['user']
        except KeyError:
            user = ZEROUSER
        else:
            user = User.from_data(user_data)
        self.user = user
    
    
    @classmethod
    def precreate(cls, webhook_id, **kwargs):
        """
        Precreates the webhook by creating a partial one with the given parameters. When the webhook will be loaded,
        the precreated one will be picked up and will be updated. If an already existing webhook would be precreated,
        it will be updated with the given parameters only if it is a partial one.
        
        Parameters
        ----------
        webhook_id : `int`, `str`
            The webhook's id.
        **kwargs : keyword parameters
            Additional predefined attributes for the webhook.
        
        Other Parameters
        ----------------
        name : `str`, Optional (Keyword only)
            The webhook's ``.name``.
        token : `str`, Optional (Keyword only)
            The webhook's ``.token``.
        
        avatar : `None`, ``Icon``, `str`, Optional (Keyword only)
            The webhook's avatar.
            
            > Mutually exclusive with `avatar_type` and `avatar_hash`.
        
        avatar_type : ``IconType``, Optional (Keyword only)
            The webhook's avatar's type.
            
            > Mutually exclusive with `avatar_type`.
        
        avatar_hash : `int`, Optional (Keyword only)
            The webhook's avatar's hash.
            
            > Mutually exclusive with `avatar`.
        
        banner : `None`, ``Icon``, `str`, Optional (Keyword only)
            The webhook's banner.
            
            > Mutually exclusive with `banner_type` and `banner_hash`.
        
        banner_type : ``IconType``, Optional (Keyword only)
            The webhook's banner's type.
            
            > Mutually exclusive with `banner_type`.
        
        banner_hash : `int`, Optional (Keyword only)
            The webhook's banner hash.
            
            > Mutually exclusive with `banner`.
        
        user : ``ClientUserBase``, Optional (Keyword only)
            The webhook's ``.user``.
        channel : ``Channel``, Optional (Keyword only)
            The webhook's ``.channel``.
        application_id : `int`, Optional (Keyword only)
            The application's id what created the webhook.
        
        Returns
        -------
        webhook : ``Webhook``
        """
        webhook_id = preconvert_snowflake(webhook_id, 'webhook_id')
        
        if kwargs:
            processable = []
            
            for attribute_name, lower_limit, upper_limit in (
                    ('name' , 0 , 80,),
                    ('token', 60, 68,),
                        ):
                
                try:
                    attribute_value = kwargs.pop(attribute_name)
                except KeyError:
                    pass
                else:
                    attribute_value = preconvert_str(attribute_value, attribute_name, lower_limit, upper_limit)
                    processable.append((attribute_name, attribute_value))
            
            cls.avatar.precovert(kwargs, processable)
            cls.banner.precovert(kwargs, processable)
            
            for attribute_name, attribute_type in (
                ('user'      , (User, Client),),
                ('channel_id', Channel   ,),
            ):
                try:
                    attribute_value = kwargs.pop(attribute_name)
                except KeyError:
                    pass
                else:
                    attribute_value = instance_or_id_to_instance(attribute_value, attribute_type, attribute_name)
                    processable.append((attribute_name, attribute_value))
            
            try:
                type_ = kwargs.pop('type')
            except KeyError:
                pass
            else:
                type_ = preconvert_preinstanced_type(type_, 'type', WebhookType)
                processable.append(('type', type_))
            
            try:
                application_id = kwargs.pop('application_id')
            except KeyError:
                pass
            else:
                application_id = preconvert_snowflake(application_id, 'application_id')
                processable.append(('application_id', application_id))
        
            if kwargs:
                raise TypeError(f'Unused or unsettable attributes: {kwargs!r}.')
        
        else:
            processable = None
        
        try:
            self = USERS[webhook_id]
        except KeyError:
            self = cls.create_empty(webhook_id)
            USERS[webhook_id] = self
        else:
            if not self.partial:
                return self
        
        if (processable is not None):
            for item in processable:
                setattr(self, *item)
        
        return self
    
    
    url = property(module_urls.webhook_url)
    
    
    @classmethod
    async def _from_follow_data(cls, data, source_channel, target_channel_id, client):
        """
        Creates the webhook, what executes cross-posts.
        
        This method is ensured after following a channel.
        
        This method is a coroutine.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Received webhook data.
        source_channel : ``Channel``
            The followed channel.
        target_channel_id : `int`
            The target channel's identifier where the webhook messages will be sent.
        client : ``Client``
            The client who created the webhook.
        
        Returns
        -------
        webhook : ``Webhook``
        """
        webhook_id = int(data['webhook_id'])
        
        guild = source_channel.guild
        if guild is None:
            try:
                extra_data = await client.http.webhook_get(webhook_id)
            except DiscordException as err:
                if err.code == ERROR_CODES.unknown_webhook:
                    #not lucky
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
            
            source_guild_data = data.get('source_guild', None)
            if source_guild_data is None:
                source_guild = None
            else:
                source_guild = WebhookSourceGuild(source_guild_data)
        
        else:
            # TODO: can it be animated if the guild's icon is animated?
            avatar_hash = guild.icon_hash
            avatar_type = guild.icon_type
            name = f'{guild.name} #{source_channel.name}'
            
            source_guild = WebhookSourceGuild._from_guild(guild)
        
        source_channel = WebhookSourceChannel._from_channel(source_channel)
        
        self = object.__new__(cls)
        self.id = webhook_id

        self.discriminator = 0
        self.avatar_hash = avatar_hash
        self.avatar_type = avatar_type
        self.banner_color = None
        self.banner_hash = 0
        self.banner_type = ICON_TYPE_NONE
        self.name = name
        
        self.channel_id = target_channel_id
        self.type = WebhookType.server
        
        self.application_id = 0
        self.source_channel = source_channel
        self.source_guild = source_guild
        self.token = ''
        self.user = client
        
        USERS[webhook_id] = self
        
        return self

    @copy_docs(UserBase._set_default_attributes)
    def _set_default_attributes(self):
        WebhookBase._set_default_attributes(self)
        
        self.application_id = 0
        self.source_guild = None
        self.source_channel = None
        self.token = ''
        self.user = ZEROUSER
