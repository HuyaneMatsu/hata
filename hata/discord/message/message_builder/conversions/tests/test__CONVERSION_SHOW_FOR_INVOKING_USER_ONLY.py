import vampytest

from ..show_for_invoking_user_only import (
    CONVERSION_SHOW_FOR_INVOKING_USER_ONLY, MESSAGE_FLAG_VALUE_SHOW_FOR_INVOKING_USER_ONLY
)


def _iter_options__set_validator():
    yield object(), []
    yield None, [0]
    yield False, [0]
    yield True, [MESSAGE_FLAG_VALUE_SHOW_FOR_INVOKING_USER_ONLY]


@vampytest._(vampytest.call_from(_iter_options__set_validator()).returning_last())
def test__CONVERSION_SHOW_FOR_INVOKING_USER_ONLY__set_validator(input_value):
    """
    Tests whether ``CONVERSION_SHOW_FOR_INVOKING_USER_ONLY.set_validator`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to test.
    
    Returns
    -------
    output : `list<int>`
    """
    return [*CONVERSION_SHOW_FOR_INVOKING_USER_ONLY.set_validator(input_value)]


def _iter_options__get_processor():
    yield 0, False
    yield MESSAGE_FLAG_VALUE_SHOW_FOR_INVOKING_USER_ONLY, True


@vampytest._(vampytest.call_from(_iter_options__get_processor()).returning_last())
def test__CONVERSION_SHOW_FOR_INVOKING_USER_ONLY__get_processor(input_value):
    """
    Tests whether ``CONVERSION_SHOW_FOR_INVOKING_USER_ONLY.get_processor`` works as intended.
    
    Parameters
    ----------
    input_value : `int`
        Value to test.
    
    Returns
    -------
    output : `bool`
    """
    return CONVERSION_SHOW_FOR_INVOKING_USER_ONLY.get_processor(input_value)
