__all__ = ('create_partial_webhook_from_id', )

from ...backend.export import export

from ..core import USERS
from ..user import ZEROUSER

from ..bases import ICON_TYPE_NONE

from .preinstanced import WebhookType
from .webhook import Webhook

@export
def create_partial_webhook_from_id(webhook_id, token, type_=WebhookType.bot, channel=None):
    """
    Creates a partial webhook from the given parameters. If the webhook with the given `webhook_id` already exists,
    then returns that instead.
    
    Parameters
    ----------
    webhook_id : `int`
        The identifier number of the webhook.
    token : `str`
        The token of the webhook.
    type_ : ``WebhookType``, Optional
        The webhook's type. Defaults to `WebhookType.bot`.
    channel : ``ChannelText`` or `None`, Optional
        The channel of the webhook. Defaults to `None`.
    
    Returns
    -------
    webhook : ``Webhook``
    """
    try:
        webhook = USERS[webhook_id]
    except KeyError:
        webhook = object.__new__(Webhook)
        
        webhook.id = webhook_id
        
        webhook.name = ''
        webhook.discriminator = 0
        webhook.application_id = 0
        webhook.avatar_hash = 0
        webhook.avatar_type = ICON_TYPE_NONE
        
        webhook.user = ZEROUSER
        webhook.channel = channel
        
        webhook.type = type_
        
        USERS[webhook_id] = webhook
    
    webhook.token = token
    return webhook
