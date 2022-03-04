__all__ = ('WebhookRepr',)

from scarletio import export

from .preinstanced import WebhookType
from .utils import create_partial_webhook_from_id
from .webhook_base import WebhookBase


@export
class WebhookRepr(WebhookBase):
    """
    Represents a Discord webhook's user representation.
    
    Attributes
    ----------
    id : `int`
        The webhook representation's unique identifier number.
    name : str
        The webhook representation's username.
    discriminator : `int`
        The webhook representation's discriminator. Given to avoid overlapping names.
    avatar_hash : `int`
        The webhook representation's avatar's hash in `uint128`.
    avatar_type : ``IconType``
        The webhook representation's avatar's type.
    banner_color : `None`, ``Color``
        The user's banner color if has any.
    banner_hash : `int`
        The user's banner's hash in `uint128`.
    banner_type : ``IconType``
        The user's banner's type.
    channel_id : `int`
        The channel, where the webhook is going to send it's messages.
    type : ``WebhookType``
        The webhook's type.
    
    Notes
    -----
    Instances of the type support weakreferencing.
    """
    __slots__ = ()
    
    def __init__(self, data, webhook_id, type_, channel_id):
        """
        Creates a webhook representation.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Included user data.
        webhook_id : `int`
            The respective webhook's identifier number.
        type_ : ``WebhookType``
            The respective webhook's type.
        channel_id : `int`
            The respective webhook's channel's identifier.
        """
        self.id = webhook_id
        self.discriminator = 0
        self.name = data['username']
        self._set_avatar(data)
        self._set_banner(data)
        self.type = type_
        self.channel_id = channel_id
        self.banner_color = None
    
    @property
    def webhook(self):
        """
        Creates a partial webhook from the webhook data included with the webhook representation.
        
        Returns
        -------
        webhook : ``Webhook``
        """
        return create_partial_webhook_from_id(self.id, '', self.type, self.channel_id)
