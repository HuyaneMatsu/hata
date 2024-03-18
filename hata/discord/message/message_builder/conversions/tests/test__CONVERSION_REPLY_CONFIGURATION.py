import vampytest

from ...reply_configuration import ReplyConfiguration

from ..reply_configuration import CONVERSION_REPLY_CONFIGURATION


def _iter_options__set_merger():
    yield (
        ReplyConfiguration(message_id = 202403090000),
        ReplyConfiguration(message_id = 202403090000),
        ReplyConfiguration(message_id = 202403090000),
    )
    yield (
        ReplyConfiguration(message_id = 202403090001),
        ReplyConfiguration(fail_fallback = True),
        ReplyConfiguration(fail_fallback = True, message_id = 202403090001),
    )


@vampytest._(vampytest.call_from(_iter_options__set_merger()).returning_last())
def test__CONVERSION_REPLY_CONFIGURATION__set_merger(input_value_0, input_value_1):
    """
    Tests whether ``CONVERSION_REPLY_CONFIGURATION.set_merger`` works as intended.
    
    Parameters
    ----------
    input_value_0 : ``ReplyConfiguration``
        Value to test.
    input_value_1 : ``ReplyConfiguration``
        Value to test.
    
    Returns
    -------
    output : ``ReplyConfiguration``
    """
    return CONVERSION_REPLY_CONFIGURATION.set_merger(input_value_0, input_value_1)


def _iter_options__serializer_optional():
    yield (
        ReplyConfiguration(message_id = 202403090002),
        [{'message_id': str(202403090002)}]
    )
    
    yield (
        ReplyConfiguration(fail_fallback = False),
        []
    )


@vampytest._(vampytest.call_from(_iter_options__serializer_optional()).returning_last())
def test__CONVERSION_REPLY_CONFIGURATION__serializer_optional(input_value):
    """
    Tests whether ``CONVERSION_REPLY_CONFIGURATION.serializer_optional`` works as intended.
    
    Parameters
    ----------
    input_value : ``ReplyConfiguration``
        Value to test.
    
    Returns
    -------
    output : `list<dict<str, object>>`
    """
    return [*CONVERSION_REPLY_CONFIGURATION.serializer_optional(input_value)]


def _iter_options__serializer_required():
    yield (
        ReplyConfiguration(message_id = 202403090002),
        {'message_id': str(202403090002)},
    )
    
    yield (
        ReplyConfiguration(fail_fallback = False),
        {'message_id': str(0)}
    )


@vampytest._(vampytest.call_from(_iter_options__serializer_required()).returning_last())
def test__CONVERSION_REPLY_CONFIGURATION__serializer_required(input_value):
    """
    Tests whether ``CONVERSION_REPLY_CONFIGURATION.serializer_required`` works as intended.
    
    Parameters
    ----------
    input_value : ``ReplyConfiguration``
        Value to test.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return CONVERSION_REPLY_CONFIGURATION.serializer_required(input_value)
