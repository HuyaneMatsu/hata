import vampytest

from ..silent import CONVERSION_SILENT, MESSAGE_FLAG_VALUE_SILENT


def _iter_options__set_validator():
    yield object(), []
    yield None, [0]
    yield False, [0]
    yield True, [MESSAGE_FLAG_VALUE_SILENT]


@vampytest._(vampytest.call_from(_iter_options__set_validator()).returning_last())
def test__CONVERSION_SILENT__set_validator(input_value):
    """
    Tests whether ``CONVERSION_SILENT.set_validator`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to test.
    
    Returns
    -------
    output : `list<int>`
    """
    return [*CONVERSION_SILENT.set_validator(input_value)]


def _iter_options__get_processor():
    yield 0, False
    yield MESSAGE_FLAG_VALUE_SILENT, True


@vampytest._(vampytest.call_from(_iter_options__get_processor()).returning_last())
def test__CONVERSION_SILENT__get_processor(input_value):
    """
    Tests whether ``CONVERSION_SILENT.get_processor`` works as intended.
    
    Parameters
    ----------
    input_value : `int`
        Value to test.
    
    Returns
    -------
    output : `bool`
    """
    return CONVERSION_SILENT.get_processor(input_value)
