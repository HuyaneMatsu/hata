import vampytest

from ...message_reference_configuration import MessageReferenceConfiguration

from ..reply_message_id import CONVERSION_REPLY_MESSAGE_ID


def _iter_options__set_validator():
    yield object(), []
    yield None, [MessageReferenceConfiguration()]
    yield 0, [MessageReferenceConfiguration(message_id = 0)]
    yield 202303090001, [MessageReferenceConfiguration(message_id = 202303090001)]


@vampytest._(vampytest.call_from(_iter_options__set_validator()).returning_last())
def test__CONVERSION_REPLY_MESSAGE_ID__set_validator(input_value):
    """
    Tests whether ``CONVERSION_REPLY_MESSAGE_ID.set_validator`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to test.
    
    Returns
    -------
    output : `list<MessageReferenceConfiguration>`
    """
    return [*CONVERSION_REPLY_MESSAGE_ID.set_validator(input_value)]


def _iter_options__get_processor():
    yield None, 0
    yield MessageReferenceConfiguration(message_id = 0), 0
    yield MessageReferenceConfiguration(message_id = 202303090002), 202303090002


@vampytest._(vampytest.call_from(_iter_options__get_processor()).returning_last())
def test__CONVERSION_REPLY_MESSAGE_ID__get_processor(input_value):
    """
    Tests whether ``CONVERSION_REPLY_MESSAGE_ID.get_processor`` works as intended.
    
    Parameters
    ----------
    input_value : `None | MessageReferenceConfiguration`
        Value to test.
    
    Returns
    -------
    output : `int`
    """
    output = CONVERSION_REPLY_MESSAGE_ID.get_processor(input_value)
    vampytest.assert_instance(output, int)
    return output
