import vampytest

from ...message_reference_configuration import MessageReferenceConfiguration

from ..message_reference_configuration import CONVERSION_MESSAGE_REFERENCE_CONFIGURATION


def _iter_options__set_merger():
    yield (
        MessageReferenceConfiguration(message_id = 202403090000),
        MessageReferenceConfiguration(message_id = 202403090000),
        MessageReferenceConfiguration(message_id = 202403090000),
    )
    yield (
        MessageReferenceConfiguration(message_id = 202403090001),
        MessageReferenceConfiguration(fail_fallback = True),
        MessageReferenceConfiguration(fail_fallback = True, message_id = 202403090001),
    )


@vampytest._(vampytest.call_from(_iter_options__set_merger()).returning_last())
def test__CONVERSION_MESSAGE_REFERENCE_CONFIGURATION__set_merger(input_value_0, input_value_1):
    """
    Tests whether ``CONVERSION_MESSAGE_REFERENCE_CONFIGURATION.set_merger`` works as intended.
    
    Parameters
    ----------
    input_value_0 : ``MessageReferenceConfiguration``
        Value to test.
    input_value_1 : ``MessageReferenceConfiguration``
        Value to test.
    
    Returns
    -------
    output : ``MessageReferenceConfiguration``
    """
    return CONVERSION_MESSAGE_REFERENCE_CONFIGURATION.set_merger(input_value_0, input_value_1)


def _iter_options__serializer_optional():
    yield (
        MessageReferenceConfiguration(message_id = 202403090002),
        [{'message_id': str(202403090002)}]
    )
    
    yield (
        MessageReferenceConfiguration(fail_fallback = False),
        []
    )


@vampytest._(vampytest.call_from(_iter_options__serializer_optional()).returning_last())
def test__CONVERSION_MESSAGE_REFERENCE_CONFIGURATION__serializer_optional(input_value):
    """
    Tests whether ``CONVERSION_MESSAGE_REFERENCE_CONFIGURATION.serializer_optional`` works as intended.
    
    Parameters
    ----------
    input_value : ``MessageReferenceConfiguration``
        Value to test.
    
    Returns
    -------
    output : `list<dict<str, object>>`
    """
    return [*CONVERSION_MESSAGE_REFERENCE_CONFIGURATION.serializer_optional(input_value)]


def _iter_options__serializer_required():
    yield (
        MessageReferenceConfiguration(message_id = 202403090002),
        {'message_id': str(202403090002)},
    )
    
    yield (
        MessageReferenceConfiguration(fail_fallback = False),
        {'message_id': str(0)}
    )


@vampytest._(vampytest.call_from(_iter_options__serializer_required()).returning_last())
def test__CONVERSION_MESSAGE_REFERENCE_CONFIGURATION__serializer_required(input_value):
    """
    Tests whether ``CONVERSION_MESSAGE_REFERENCE_CONFIGURATION.serializer_required`` works as intended.
    
    Parameters
    ----------
    input_value : ``MessageReferenceConfiguration``
        Value to test.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return CONVERSION_MESSAGE_REFERENCE_CONFIGURATION.serializer_required(input_value)
