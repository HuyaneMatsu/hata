import vampytest

from ....message.message.fields import validate_channel_id, validate_id

from ...conversion_helpers.converters import get_converter_id, put_converter_id

from ..message import CHANNEL_ID_CONVERSION, COUNT_CONVERSION, ID_CONVERSION, MESSAGE_CONVERSIONS


def test__MESSAGE_CONVERSIONS():
    """
    Tests whether `MESSAGE_CONVERSIONS` contains conversion for every expected key.
    """
    vampytest.assert_eq(
        {*MESSAGE_CONVERSIONS.get_converters.keys()},
        {'channel_id', 'count', 'message_id'}
    )


# ---- channel_id ----

def test__CHANNEL_ID_CONVERSION__generic():
    """
    Tests whether ``CHANNEL_ID_CONVERSION`` works as intended.
    """
    vampytest.assert_is(CHANNEL_ID_CONVERSION.get_converter, get_converter_id)
    vampytest.assert_is(CHANNEL_ID_CONVERSION.put_converter, put_converter_id)
    vampytest.assert_is(CHANNEL_ID_CONVERSION.validator, validate_channel_id)


# ---- count ----

def _iter_options__count__get_converter():
    count = 123
    yield 0, 0
    yield count, count
    yield None, 0


@vampytest._(vampytest.call_from(_iter_options__count__get_converter()).returning_last())
def test__COUNT_CONVERSION__get_converter(input_value):
    """
    Tests whether `COUNT_CONVERSION.get_converter` works as intended.
    
    Parameters
    ----------
    input_value : `int`
        Raw value.
    
    Returns
    -------
    output : `int`
    """
    return COUNT_CONVERSION.get_converter(input_value)


def _iter_options__count__put_converter():
    count = 123
    yield 0, 0
    yield count, count


@vampytest._(vampytest.call_from(_iter_options__count__put_converter()).returning_last())
def test__COUNT_CONVERSION__put_converter(input_value):
    """
    Tests whether `COUNT_CONVERSION.put_converter` works as intended.
    
    Parameters
    ----------
    input_value : `int`
        Processed value.
    
    Returns
    -------
    output : `int`
    """
    return COUNT_CONVERSION.put_converter(input_value)


def _iter_options__count__validator__passing():
    count = 1123
    yield 0, 0
    yield count, count


def _iter_options__count__validator__type_error():
    yield 12.6


def _iter_options__count__validator__value_error():
    yield -12


@vampytest._(vampytest.call_from(_iter_options__count__validator__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__count__validator__type_error()).raising(TypeError))
@vampytest._(vampytest.call_from(_iter_options__count__validator__value_error()).raising(ValueError))
def test__COUNT_CONVERSION__validator(input_value):
    """
    Tests whether `COUNT_CONVERSION.validator` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : `int`
    
    Raises
    ------
    TypeError
    ValueError
    """
    return COUNT_CONVERSION.validator(input_value)


# ---- id ----

def test__ID_CONVERSION__generic():
    """
    Tests whether ``ID_CONVERSION`` works as intended.
    """
    vampytest.assert_is(ID_CONVERSION.get_converter, get_converter_id)
    vampytest.assert_is(ID_CONVERSION.put_converter, put_converter_id)
    vampytest.assert_is(ID_CONVERSION.validator, validate_id)
