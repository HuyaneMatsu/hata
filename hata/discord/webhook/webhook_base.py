__all__ = ('WebhookBase',)

from scarletio import copy_docs, include

from ..core import CHANNELS
from ..permission.permission import PERMISSION_MASK_USE_EXTERNAL_EMOJIS
from ..user import UserBase

from .preinstanced import WebhookType


ChannelType = include('ChannelType')
create_partial_channel_from_id = include('create_partial_channel_from_id')


class WebhookBase(UserBase):
    """
    Base class for webhook like-types.
    
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
    """
    __slots__ = ('channel_id', 'type',)
    
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
        
        emoji_roles = emoji.emoji_roles
        if (emoji_roles is not None):
            return False
        
        guild = self.guild
        if guild is None:
            return False
        
        default_role = guild.default_role
        if default_role & PERMISSION_MASK_USE_EXTERNAL_EMOJIS:
            return True
        
        return False
    
    
    @copy_docs(UserBase._set_default_attributes)
    def _set_default_attributes(self):
        UserBase._set_default_attributes(self)
        
        self.channel_id = 0
        self.type = WebhookType.none
