__all__ = ()

from ...webhook import WebhookType

from .shared import _convert_preinstanced, convert_icon, convert_nothing, convert_snowflake


def convert_webhook_type(name, data):
    return _convert_preinstanced('type', data, WebhookType)


WEBHOOK_CONVERTERS = {
    'application_id': convert_snowflake,
    'avatar_hash': convert_icon,
    'channel_id': convert_snowflake,
    'id': convert_snowflake,
    'name': convert_nothing,
    'type': convert_webhook_type,
}
