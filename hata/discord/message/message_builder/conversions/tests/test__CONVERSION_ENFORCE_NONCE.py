import vampytest

from ..enforce_nonce import CONVERSION_ENFORCE_NONCE


def _iter_options__set_validator():
    yield object(), []
    yield None, [False]
    yield False, [False]
    yield True, [True]


@vampytest._(vampytest.call_from(_iter_options__set_validator()).returning_last())
def test__CONVERSION_ENFORCE_NONCE__set_validator(input_value):
    """
    Tests whether ``CONVERSION_ENFORCE_NONCE.set_validator`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to test.
    
    Returns
    -------
    output : `list<bool>`
    """
    return [*CONVERSION_ENFORCE_NONCE.set_validator(input_value)]


def _iter_options__serializer_optional():
    yield False, []
    yield True, [True]


@vampytest._(vampytest.call_from(_iter_options__serializer_optional()).returning_last())
def test__CONVERSION_ENFORCE_NONCE__serializer_optional(input_value):
    """
    Tests whether ``CONVERSION_ENFORCE_NONCE.serializer_optional`` works as intended.
    
    Parameters
    ----------
    input_value : `bool`
        Value to test.
    
    Returns
    -------
    output : `list<bool>`
    """
    return [*CONVERSION_ENFORCE_NONCE.serializer_optional(input_value)]


def _iter_options__serializer_required():
    yield False, False
    yield True, True


@vampytest._(vampytest.call_from(_iter_options__serializer_required()).returning_last())
def test__CONVERSION_ENFORCE_NONCE__serializer_required(input_value):
    """
    Tests whether ``CONVERSION_ENFORCE_NONCE.serializer_required`` works as intended.
    
    Parameters
    ----------
    input_value : `bool`
        Value to test.
    
    Returns
    -------
    output : `bool`
    """
    return CONVERSION_ENFORCE_NONCE.serializer_required(input_value)
