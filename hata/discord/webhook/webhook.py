__all__ = ('Webhook', )

from ...backend.export import export, include

from ..core import USERS
from ..user import User, ZEROUSER, ClientUserBase
from ..exceptions import DiscordException, ERROR_CODES
from ..preconverters import preconvert_snowflake, preconvert_str, preconvert_preinstanced_type
from ..bases import ICON_TYPE_NONE, Icon
from ..http.urls import WEBHOOK_URL_PATTERN
from ..http import urls as module_urls

from .webhook_base import WebhookBase
from .preinstanced import WebhookType

create_partial_webhook_from_id = include('create_partial_webhook_from_id')
create_partial_channel_from_id = include('create_partial_channel_from_id')
ChannelText = include('ChannelText')

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
    avatar_type : `bool`
        The webhook's avatar's type.
    channel : `None` or ``ChannelText``
        The channel, where the webhook is going to send it's messages.
    application_id : `int`
        The application's id what created the webhook. Defaults to `0` if not applicable.
    token : `str`
        The webhooks's token. You need an `id` and a `token` to send webhook message. Defaults to empty string.
    type : ``WebhookType``
        The webhook's type.
    user : ``Client`` or ``User``
        The creator of the webhook, or `ZEROUSER` if unknown.
    
    Notes
    -----
    Instances of this class are weakreferable.
    """
    __slots__ = ('application_id', 'token', 'type', 'user', )
    
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
        
        self._update_no_return(data)
        self.type = WebhookType.get(data['type'])
        
        application_id = data.get('application_id', None)
        if application_id is None:
            application_id = 0
        else:
            application_id = int(application_id)
        self.application_id = application_id
        
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
        webhook : `None` or ``Webhook``
        """
        result = WEBHOOK_URL_PATTERN.fullmatch(url)
        if result is None:
            return None
        
        webhook_id = int(result.group(1))
        webhook_token = result.group(2)
        
        return create_partial_webhook_from_id(webhook_id, webhook_token)
    
    def _update_no_return(self, data):
        """
        Updates the webhook with the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Received webhook data.
        """
        self.channel = channel = create_partial_channel_from_id(int(data['channel_id']), 0)
        if channel.clients:
            channel.guild.webhooks[self.id] = self
        
        token = data.get('token', None)
        if (token is not None):
            self.token = token
        
        name = data['name']
        if name is None:
            name = ''
        
        self.name = name
        
        self.discriminator = 0
        
        self._set_avatar(data)
        
        try:
            user_data = data['user']
        except KeyError:
            user = ZEROUSER
        else:
            user = User(user_data)
        self.user = user
    
    
    @classmethod
    def precreate(cls, webhook_id, **kwargs):
        """
        Precreates the webhook by creating a partial one with the given parameters. When the webhook will be loaded,
        the precreated one will be picked up and will be updated. If an already existing webhook would be precreated,
        it will be updated with the given parameters only if it is a partial one.
        
        Parameters
        ----------
        webhook_id : `int` or `str`
            The webhook's id.
        **kwargs : keyword parameters
            Additional predefined attributes for the webhook.
        
        Other Parameters
        ----------------
        name : `str`, Optional (Keyword only)
            The webhook's ``.name``.
        token : `str`, Optional (Keyword only)
            The webhook's ``.token``.
        avatar : `None`, ``Icon`` or `str`, Optional (Keyword only)
            The webhooks's avatar. Mutually exclusive with `avatar_type` and `avatar_hash`.
        avatar_type : ``IconType``, Optional (Keyword only)
            The webhooks's avatar's type. Mutually exclusive with `avatar_type`.
        avatar_hash : `int`, Optional (Keyword only)
            The webhooks's avatar hash. Mutually exclusive with `avatar`.
        user : ``Client`` or ``User``, Optional (Keyword only)
            The webhook's ``.user``.
        channel : ``ChannelText``, Optional (Keyword only)
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
            
            for key, details in (
                    ('name' , (0 , 80,)),
                    ('token', (60, 68,)),
                        ):
                
                try:
                    value = kwargs.pop(key)
                except KeyError:
                    pass
                else:
                    value = preconvert_str(value, key, *details)
                    processable.append((key, value))
            
            cls.avatar.precovert(kwargs, processable)
            
            for key, type_ in (
                    ('user', (ClientUserBase)),
                    ('channel', ChannelText),
                        ):
                try:
                    value = kwargs.pop(key)
                except KeyError:
                    pass
                else:
                    if not isinstance(value,type_):
                        raise TypeError(f'`{key}` can be instance of: {type_!r}, got: {value.__class__.__name__}.')
                    processable.append((key, value))
            
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
                raise TypeError(f'Unused or unsettable attributes: {kwargs}.')
        
        else:
            processable = None
        
        try:
            self = USERS[webhook_id]
        except KeyError:
            self = object.__new__(cls)
            
            self.id = webhook_id
            self.token = ''
            self.name = ''
            self.discriminator = 0
            self.avatar_hash = 0
            self.avatar_type = ICON_TYPE_NONE
            self.user = ZEROUSER
            self.channel = None
            self.type = WebhookType.bot
            self.application_id = 0
            
            USERS[webhook_id] = self
        else:
            if not self.partial:
                return self
        
        if (processable is not None):
            for item in processable:
                setattr(self, *item)
        
        return self
    
    
    def _delete(self):
        """
        Removes the webhook's references.
        """
        channel = self.channel
        if channel is None:
            return
        guild = channel.guild
        if (guild is not None):
            try:
                del guild.webhooks[self.id]
            except KeyError:
                pass
        self.channel = None
        self.user = ZEROUSER
    
    url = property(module_urls.webhook_url)
    
    @classmethod
    async def _from_follow_data(cls, data, source_channel, target_channel, client):
        """
        Creates the webhook, what executes cross-posts.
        
        This method is ensured after following a channel.
        
        This method is a coroutine.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Received webhook data.
        source_channel : ``ChannelText`` instance
            The followed channel.
        target_channel : ``ChannelText`` instance
            The target channel where the webhook messages will be sent.
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
        else:
            # TODO: can it be animated if the guild's icon is animated?
            avatar_hash = guild.icon_hash
            avatar_type = guild.icon_type
            name = f'{guild.name} #{source_channel.name}'
        
        self = object.__new__(cls)
        self.id = webhook_id
        self.name = name
        self.discriminator = 0
        self.avatar_hash = avatar_hash
        self.avatar_type = avatar_type
        self.channel = target_channel
        self.token = ''
        self.user = client
        self.type = WebhookType.server
        self.application_id = 0
        
        guild = target_channel.guild
        if (guild is not None):
            guild.webhooks[webhook_id] = self
        
        USERS[webhook_id] = self
        
        return self
