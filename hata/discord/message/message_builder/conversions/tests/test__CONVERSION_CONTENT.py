import vampytest

from ..content import CONVERSION_CONTENT


def _iter_options__set_type_processor():
    yield '', None
    yield 'mister', 'mister'


@vampytest._(vampytest.call_from(_iter_options__set_type_processor()).returning_last())
def test__CONVERSION_CONTENT__set_type_processor(input_value):
    """
    Tests whether ``CONVERSION_CONTENT.set_type_processor`` works as intended.
    
    Parameters
    ----------
    input_value : `str`
        Value to test.
    
    Returns
    -------
    output : `None | str`
    """
    return CONVERSION_CONTENT.set_type_processor(input_value)


def _iter_options__set_validator():
    yield object(), []
    yield None, [None]
    yield '', [None]
    yield 'mister', ['mister']


@vampytest._(vampytest.call_from(_iter_options__set_validator()).returning_last())
def test__CONVERSION_CONTENT__set_validator(input_value):
    """
    Tests whether ``CONVERSION_CONTENT.set_validator`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to test.
    
    Returns
    -------
    output : `list<None | str>`
    """
    return [*CONVERSION_CONTENT.set_validator(input_value)]


def _iter_options__serializer_optional():
    yield None, []
    yield 'mister', ['mister']


@vampytest._(vampytest.call_from(_iter_options__serializer_optional()).returning_last())
def test__CONVERSION_CONTENT__serializer_optional(input_value):
    """
    Tests whether ``CONVERSION_CONTENT.serializer_optional`` works as intended.
    
    Parameters
    ----------
    input_value : `None | str`
        Value to test.
    
    Returns
    -------
    output : `list<str>`
    """
    return [*CONVERSION_CONTENT.serializer_optional(input_value)]


def _iter_options__serializer_required():
    yield None, ''
    yield 'mister', 'mister'


@vampytest._(vampytest.call_from(_iter_options__serializer_required()).returning_last())
def test__CONVERSION_CONTENT__serializer_required(input_value):
    """
    Tests whether ``CONVERSION_CONTENT.serializer_required`` works as intended.
    
    Parameters
    ----------
    input_value : `None | str`
        Value to test.
    
    Returns
    -------
    output : `str`
    """
    return CONVERSION_CONTENT.serializer_required(input_value)
