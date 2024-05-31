import vampytest

from ...message_reference_configuration import MessageReferenceConfiguration

from ..reply_fail_fallback import CONVERSION_REPLY_FAIL_FALLBACK


def _iter_options__set_validator():
    yield object(), []
    yield None, [MessageReferenceConfiguration()]
    yield False, [MessageReferenceConfiguration(fail_fallback = False)]
    yield True, [MessageReferenceConfiguration(fail_fallback = True)]


@vampytest._(vampytest.call_from(_iter_options__set_validator()).returning_last())
def test__CONVERSION_REPLY_FAIL_FALLBACK__set_validator(input_value):
    """
    Tests whether ``CONVERSION_REPLY_FAIL_FALLBACK.set_validator`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to test.
    
    Returns
    -------
    output : `list<MessageReferenceConfiguration>`
    """
    return [*CONVERSION_REPLY_FAIL_FALLBACK.set_validator(input_value)]


def _iter_options__get_processor():
    yield None, False
    yield MessageReferenceConfiguration(fail_fallback = False), False
    yield MessageReferenceConfiguration(fail_fallback = True), True


@vampytest._(vampytest.call_from(_iter_options__get_processor()).returning_last())
def test__CONVERSION_REPLY_FAIL_FALLBACK__get_processor(input_value):
    """
    Tests whether ``CONVERSION_REPLY_FAIL_FALLBACK.get_processor`` works as intended.
    
    Parameters
    ----------
    input_value : `None | MessageReferenceConfiguration`
        Value to test.
    
    Returns
    -------
    output : `bool`
    """
    output = CONVERSION_REPLY_FAIL_FALLBACK.get_processor(input_value)
    vampytest.assert_instance(output, bool)
    return output
