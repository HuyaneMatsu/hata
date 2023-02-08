__all__ = ('create_partial_webhook_from_id', )

import warnings

from scarletio import export

from ...core import USERS

from .preinstanced import WebhookType
from .webhook import Webhook


@export
def create_partial_webhook_from_id(webhook_id, token, *, channel_id = 0, type_ = ..., webhook_type = WebhookType.bot):
    """
    Creates a partial webhook from the given parameters. If the webhook with the given `webhook_id` already exists,
    then returns that instead.
    
    Parameters
    ----------
    webhook_id : `int`
        The identifier number of the webhook.
    token : `str`
        The token of the webhook.
    webhook_type : ``WebhookType`` = `WebhookType.bot`, Optional (Keyword only)
        The webhook's type. Defaults to `WebhookType.bot`.
    channel_id : `int` = `0`, Optional (Keyword only)
        The webhook's channel's identifier. Defaults to `0`.
    
    Returns
    -------
    webhook : ``Webhook``
    """
    if type_ is not ...:
        warnings.warn(
            (
                f'`create_partial_webhook_from_id`\'s `type_` is deprecated and will be removed in 2023 Jul.'
                f'Please use `webhook_type` instead.'
            ),
            FutureWarning,
            stacklevel = 2,
        )
        webhook_type = type_
    
    try:
        webhook = USERS[webhook_id]
    except KeyError:
        webhook = Webhook._create_empty(webhook_id)
        webhook.channel_id = channel_id
        webhook.type = webhook_type
        
        USERS[webhook_id] = webhook
    
    webhook.token = token
    return webhook
