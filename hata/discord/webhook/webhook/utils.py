__all__ = ('create_partial_webhook_from_id', )

from scarletio import export

from ...core import USERS

from .preinstanced import WebhookType
from .webhook import Webhook


@export
def create_partial_webhook_from_id(webhook_id, token, *, channel_id = 0, webhook_type = WebhookType.bot):
    """
    Creates a partial webhook from the given parameters. If the webhook with the given `webhook_id` already exists,
    then returns that instead.
    
    Parameters
    ----------
    webhook_id : `int`
        The identifier number of the webhook.
    token : `str`
        The token of the webhook.
    channel_id : `int` = `0`, Optional (Keyword only)
        The webhook's channel's identifier.
    webhook_type : ``WebhookType`` = `WebhookType.bot`, Optional (Keyword only)
        The webhook's type.
    
    Returns
    -------
    webhook : ``Webhook``
    """
    try:
        webhook = USERS[webhook_id]
    except KeyError:
        webhook = Webhook._create_empty(webhook_id)
        webhook.channel_id = channel_id
        webhook.type = webhook_type
        
        USERS[webhook_id] = webhook
    
    webhook.token = token
    return webhook
