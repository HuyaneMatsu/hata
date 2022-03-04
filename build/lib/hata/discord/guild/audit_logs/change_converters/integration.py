__all__ = ()

from .shared import convert_nothing


INTEGRATION_CONVERTERS = {
    'enable_emoticons': convert_nothing,
    'expire_behavior': convert_nothing,
    'expire_grace_period': convert_nothing,
}
