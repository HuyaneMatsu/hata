__all__ = ('WebhookBase',)

from scarletio import copy_docs, include

from ...bases import PlaceHolder
from ...core import CHANNELS
from ...permission.permission import PERMISSION_MASK_USE_EXTERNAL_EMOJIS
from ...user import UserBase, ZEROUSER
from ...user.user.fields import validate_webhook_name

from .fields import validate_channel_id, validate_type
from .preinstanced import WebhookType


ChannelType = include('ChannelType')
create_partial_channel_from_id = include('create_partial_channel_from_id')


class WebhookBase(UserBase):
    """
    Base class for webhook like-types.
    
    Attributes
    ----------
    avatar_hash : `int`
        The webhook's avatar's hash in `uint128`.
    avatar_type : ``IconType``
        The webhook's avatar's type.
    channel_id : `int`
        The channel's identifier, where the webhook is going to send it's messages.
    id : `int`
        The webhook's unique identifier number.
    name : str
        The webhook's username.
    type : ``WebhookType``
        The webhook's type.
    """
    __slots__ = ('channel_id', 'type',)
    
    def __new__(
        cls,
        *,
        avatar = ...,
        channel_id = ...,
        name = ...,
        webhook_type = ...
    ):
        """
        Creates a new partial webhook base with the given fields.
        
        Parameters
        ----------
        channel_id : `int`, Optional (Keyword only)
            The channel's identifier, where the webhook is going to send it's messages.
        avatar : `None`, ``Icon``, `str`, `bytes-like`, Optional (Keyword only)
            The user's avatar.
        name : `str`, Optional (Keyword only)
            The user's name.
        webhook_type : ``WebhookType``, `int`, Optional (Keyword only)
            The webhook's type.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # channel_id
        if channel_id is ...:
            channel_id = 0
        else:
            channel_id = validate_channel_id(channel_id)
        
        # name | Do not pass `name` down since webhooks allow longer names.
        if name is ...:
            name = ''
        else:
            name = validate_webhook_name(name)
        
        # webhook_type
        if webhook_type is ...:
            webhook_type = WebhookType.none
        else:
            webhook_type = validate_type(webhook_type)
        
        # Construct
        self = UserBase.__new__(
            cls,
            avatar = avatar,
            name = ...,
        )
        self.channel_id = channel_id
        self.name = name
        self.type = webhook_type
        return self
    
    
    @copy_docs(UserBase._set_default_attributes)
    def _set_default_attributes(self):
        UserBase._set_default_attributes(self)
        
        self.channel_id = 0
        self.type = WebhookType.none
    
    
    @copy_docs(UserBase.copy)
    def copy(self):
        new = UserBase.copy(self)
        new.channel_id = self.channel_id
        new.type = self.type
        return new
    
    
    def copy_with(
        self,
        *,
        avatar = ...,
        channel_id = ...,
        name = ...,
        webhook_type = ...,
    ):
        """
        Copies the webhook base with the given fields.
        
        Parameters
        ----------
        channel_id : `int`, Optional (Keyword only)
            The channel's identifier, where the webhook is going to send it's messages.
        avatar : `None`, ``Icon``, `str`, `bytes-like`, Optional (Keyword only)
            The user's avatar.
        name : `str`, Optional (Keyword only)
            The user's name.
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
        # channel_id
        if channel_id is ...:
            channel_id = self.channel_id
        else:
            channel_id = validate_channel_id(channel_id)
        
        # name | Do not pass `name` down since webhooks allow longer names.
        if name is ...:
            name = self.name
        else:
            name = validate_webhook_name(name)
        
        # webhook_type
        if webhook_type is ...:
            webhook_type = self.type
        else:
            webhook_type = validate_type(webhook_type)
        
        # Construct
        new = UserBase.copy_with(
            self,
            avatar = avatar,
            name = ...,
        )
        new.channel_id = channel_id
        new.name = name
        new.type = webhook_type
        return new
    
    
    @copy_docs(UserBase._get_hash_partial)
    def _get_hash_partial(self):
        hash_value = UserBase._get_hash_partial(self)
        
        # channel_id
        hash_value ^= self.channel_id
        
        # type
        hash_value ^= hash(self.type)
        
        return hash_value
    
    
    @copy_docs(UserBase._compare_attributes)
    def _compare_attributes(self, other):
        if not self._compare_user_attributes_extended(other):
            return False
        
        if isinstance(other, WebhookBase):
            return self._compare_webhook_attributes(other)
        
        return True
    
    
    def _compare_webhook_attributes(self, other):
        """
        Compares the two user's webhook attributes (excluding id obviously).
        
        Parameters
        ----------
        other : `instance<type<self>>`
            The other user.
        
        Returns
        -------
        is_equal : `bool`
        """
        if self.application_id != other.application_id:
            return False
        
        if self.channel_id != other.channel_id:
            return False
        
        if self.source_channel != other.source_channel:
            return False
        
        if self.source_guild != other.source_guild:
            return False
        
        if self.token != other.token:
            return False
        
        if self.type is not other.type:
            return False
        
        if self.user != other.user:
            return False
        
        return True
    
    # Placeholder
    
    application_id = PlaceHolder(
        0,
        """
        Returns the application's identifier that created the webhook.
        
        Returns
        -------
        application_id : `int`
        """
    )
    
    
    source_channel = PlaceHolder(
        None,
        """
        Returns the representation of the webhook's source channel.
        
        Returns
        -------
        source_channel : `None`, ``WebhookSourceChannel``
        """
    )
    
    
    source_guild = PlaceHolder(
        None,
        """
        Returns the representation of the webhook's source guild.
        
        Returns
        -------
        source_guild : `None`, ``WebhookSourceGuild``
        """
    )
    
    
    token = PlaceHolder(
        '',
        """
        Returns the webhook's token.
        
        Returns
        -------
        token : `str`
        """
    )
    
    
    user = PlaceHolder(
        ZEROUSER,
        """
        Returns the creator of the webhook.
        
        Returns
        -------
        user : ``ClientUserBase``
        """
    )
    
    # Extra
    
    @property
    def bot(self):
        """
        Webhooks are always bots.
        
        Returns
        -------
        bot : `bool`
        """
        return True
    
    
    @property
    def partial(self):
        """
        Returns whether the webhook is partial.
        
        A webhook is partial, if it's respective guild is unknown.
        
        Returns
        -------
        partial : `bool`
        """
        try:
            channel = CHANNELS[self.channel_id]
        except KeyError:
            return True
        
        if channel.guild is None:
            return True
        
        return False
    
    
    @property
    def channel(self):
        """
        Returns the webhook's channel if applicable.
        
        Returns
        -------
        channel : ``Channel``
        """
        return create_partial_channel_from_id(self.channel_id, ChannelType.unknown, 0)
    
    
    @property
    def guild(self):
        """
        Returns the webhook's guild if applicable.
        
        Returns
        -------
        guild : `None`, ``Guild``
        """
        try:
            channel = CHANNELS[self.channel_id]
        except KeyError:
            pass
        else:
            return channel.guild
    
    
    @copy_docs(UserBase.can_use_emoji)
    def can_use_emoji(self, emoji):
        if emoji.is_unicode_emoji():
            return True
        
        role_ids = emoji.role_ids
        if (role_ids is not None):
            return False
        
        guild = self.guild
        if guild is None:
            return False
        
        default_role = guild.default_role
        if (default_role is None):
            return False
        
        if (default_role & PERMISSION_MASK_USE_EXTERNAL_EMOJIS):
            return True
        
        return False
