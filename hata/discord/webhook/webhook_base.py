__all__ = ('WebhookBase',)

from ...backend.utils import copy_docs

from ..user import UserBase

from .preinstanced import WebhookType

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
    banner_hash : `int`
        The user's banner's hash in `uint128`.
    banner_type : ``IconType``
        The user's banner's type.
    channel : `None` or ``ChannelText``
        The channel, where the webhook is going to send it's messages.
    type : ``WebhookType``
        The webhook's type.
    """
    __slots__ = ('channel', 'type',)
    
    @property
    def is_bot(self):
        """
        Webhooks are always bots.
        
        Returns
        -------
        is_bot : `bool`
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
        channel = self.channel
        if channel is None:
            return True
        
        if channel.guild is None:
            return True
        
        return False
    
    
    @property
    def guild(self):
        """
        Returns the webhook's guild if applicable.
        
        Returns
        -------
        guild : `None` or ``Guild``
        """
        channel = self.channel
        if channel is None:
            return
        
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
        if (default_role.can_use_external_emojis):
            return True
        
        return False
    
    
    @copy_docs(UserBase._set_default_attributes)
    def _set_default_attributes(self):
        UserBase._set_default_attributes(self)
        
        self.channel = None
        self.type = WebhookType.none
