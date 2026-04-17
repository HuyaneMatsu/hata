import vampytest

from ..tts import CONVERSION_TTS


def _iter_options__set_validator():
    yield object(), []
    yield None, [False]
    yield False, [False]
    yield True, [True]


@vampytest._(vampytest.call_from(_iter_options__set_validator()).returning_last())
def test__CONVERSION_TTS__set_validator(input_value):
    """
    Tests whether ``CONVERSION_TTS.set_validator`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to test.
    
    Returns
    -------
    output : `list<bool>`
    """
    return [*CONVERSION_TTS.set_validator(input_value)]


def _iter_options__serializer_optional():
    yield False, []
    yield True, [True]


@vampytest._(vampytest.call_from(_iter_options__serializer_optional()).returning_last())
def test__CONVERSION_TTS__serializer_optional(input_value):
    """
    Tests whether ``CONVERSION_TTS.serializer_optional`` works as intended.
    
    Parameters
    ----------
    input_value : `bool`
        Value to test.
    
    Returns
    -------
    output : `list<bool>`
    """
    return [*CONVERSION_TTS.serializer_optional(input_value)]


def _iter_options__serializer_required():
    yield False, False
    yield True, True


@vampytest._(vampytest.call_from(_iter_options__serializer_required()).returning_last())
def test__CONVERSION_TTS__serializer_required(input_value):
    """
    Tests whether ``CONVERSION_TTS.serializer_required`` works as intended.
    
    Parameters
    ----------
    input_value : `bool`
        Value to test.
    
    Returns
    -------
    output : `bool`
    """
    return CONVERSION_TTS.serializer_required(input_value)
