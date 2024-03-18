import vampytest

from ..suppress_embeds import CONVERSION_SUPPRESS_EMBEDS, MESSAGE_FLAG_VALUE_SUPPRESS_EMBEDS


def _iter_options__set_validator():
    yield object(), []
    yield None, [0]
    yield False, [0]
    yield True, [MESSAGE_FLAG_VALUE_SUPPRESS_EMBEDS]


@vampytest._(vampytest.call_from(_iter_options__set_validator()).returning_last())
def test__CONVERSION_SUPPRESS_EMBEDS__set_validator(input_value):
    """
    Tests whether ``CONVERSION_SUPPRESS_EMBEDS.set_validator`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to test.
    
    Returns
    -------
    output : `list<int>`
    """
    return [*CONVERSION_SUPPRESS_EMBEDS.set_validator(input_value)]


def _iter_options__get_processor():
    yield 0, False
    yield MESSAGE_FLAG_VALUE_SUPPRESS_EMBEDS, True


@vampytest._(vampytest.call_from(_iter_options__get_processor()).returning_last())
def test__CONVERSION_SUPPRESS_EMBEDS__get_processor(input_value):
    """
    Tests whether ``CONVERSION_SUPPRESS_EMBEDS.get_processor`` works as intended.
    
    Parameters
    ----------
    input_value : `int`
        Value to test.
    
    Returns
    -------
    output : `bool`
    """
    return CONVERSION_SUPPRESS_EMBEDS.get_processor(input_value)
