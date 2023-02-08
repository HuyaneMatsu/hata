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
    avatar_hash : `int`
        The webhook representation's avatar's hash in `uint128`.
    avatar_type : ``IconType``
        The webhook representation's avatar's type.
    channel_id : `int`
        The channel, where the webhook is going to send it's messages.
    id : `int`
        The webhook representation's unique identifier number.
    name : str
        The webhook representation's username.
    type : ``WebhookType``
        The webhook's type.
    
    Notes
    -----
    Instances of the type support weakreferencing.
    """
    __slots__ = ()
    
    @classmethod
    def from_data(cls, data, webhook_id, webhook_type, channel_id):
        """
        Creates a webhook representation.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Included user data.
        webhook_id : `int`
            The respective webhook's identifier number.
        webhook_type : ``WebhookType``
            The respective webhook's type.
        channel_id : `int`
            The respective webhook's channel's identifier.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self._update_attributes(data)
        self.channel_id = channel_id
        self.id = webhook_id
        self.type = webhook_type
        return self
    
    
    @property
    def webhook(self):
        """
        Creates a partial webhook from the webhook data included with the webhook representation.
        
        Returns
        -------
        webhook : ``Webhook``
        """
        return create_partial_webhook_from_id(self.id, '', webhook_type = self.type, channel_id = self.channel_id)
