import vampytest

from ..thread_name import CONVERSION_THREAD_NAME


def _iter_options__set_validator():
    yield object(), []
    yield None, ['']
    yield '', ['']
    yield 'mister', ['mister']


@vampytest._(vampytest.call_from(_iter_options__set_validator()).returning_last())
def test__CONVERSION_THREAD_NAME__set_validator(input_value):
    """
    Tests whether ``CONVERSION_THREAD_NAME.set_validator`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to test.
    
    Returns
    -------
    output : `list<None | str>`
    """
    return [*CONVERSION_THREAD_NAME.set_validator(input_value)]


def _iter_options__serializer_optional():
    yield '', ['']
    yield 'mister', ['mister']


@vampytest._(vampytest.call_from(_iter_options__serializer_optional()).returning_last())
def test__CONVERSION_THREAD_NAME__serializer_optional(input_value):
    """
    Tests whether ``CONVERSION_THREAD_NAME.serializer_optional`` works as intended.
    
    Parameters
    ----------
    input_value : `str`
        Value to test.
    
    Returns
    -------
    output : `list<str>`
    """
    return [*CONVERSION_THREAD_NAME.serializer_optional(input_value)]


def _iter_options__serializer_required():
    yield '', ''
    yield 'mister', 'mister'


@vampytest._(vampytest.call_from(_iter_options__serializer_required()).returning_last())
def test__CONVERSION_THREAD_NAME__serializer_required(input_value):
    """
    Tests whether ``CONVERSION_THREAD_NAME.serializer_required`` works as intended.
    
    Parameters
    ----------
    input_value : `str`
        Value to test.
    
    Returns
    -------
    output : `str`
    """
    return CONVERSION_THREAD_NAME.serializer_required(input_value)
