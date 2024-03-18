import vampytest

from ..nonce import CONVERSION_NONCE


def _iter_options__set_validator():
    yield object(), []
    yield None, [None]
    yield '', [None]
    yield 'mister', ['mister']


@vampytest._(vampytest.call_from(_iter_options__set_validator()).returning_last())
def test__CONVERSION_NONCE__set_validator(input_value):
    """
    Tests whether ``CONVERSION_NONCE.set_validator`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to test.
    
    Returns
    -------
    output : `list<None | str>`
    """
    return [*CONVERSION_NONCE.set_validator(input_value)]


def _iter_options__serializer_optional():
    yield None, []
    yield 'mister', ['mister']


@vampytest._(vampytest.call_from(_iter_options__serializer_optional()).returning_last())
def test__CONVERSION_NONCE__serializer_optional(input_value):
    """
    Tests whether ``CONVERSION_NONCE.serializer_optional`` works as intended.
    
    Parameters
    ----------
    input_value : `None | str`
        Value to test.
    
    Returns
    -------
    output : `list<str>`
    """
    return [*CONVERSION_NONCE.serializer_optional(input_value)]


def _iter_options__serializer_required():
    yield None, ''
    yield 'mister', 'mister'


@vampytest._(vampytest.call_from(_iter_options__serializer_required()).returning_last())
def test__CONVERSION_NONCE__serializer_required(input_value):
    """
    Tests whether ``CONVERSION_NONCE.serializer_required`` works as intended.
    
    Parameters
    ----------
    input_value : `None | str`
        Value to test.
    
    Returns
    -------
    output : `str`
    """
    return CONVERSION_NONCE.serializer_required(input_value)
