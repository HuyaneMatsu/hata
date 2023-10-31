import vampytest

from ....soundboard.soundboard_sound.fields import (
    validate_available, validate_id, validate_name, validate_user_id, validate_volume
)

from ...conversion_helpers.converters import get_converter_id, get_converter_name, put_converter_id, put_converter_name

from ..soundboard_sound import (
    AVAILABLE_CONVERSION, ID_CONVERSION, NAME_CONVERSION, SOUNDBOARD_SOUND_CONVERSIONS, USER_ID_CONVERSION,
    VOLUME_CONVERSION
)


def test__SOUNDBOARD_SOUND_CONVERSIONS():
    """
    Tests whether `SOUNDBOARD_SOUND_CONVERSIONS` contains conversion for every expected key.
    """
    vampytest.assert_eq(
        {*SOUNDBOARD_SOUND_CONVERSIONS.get_converters.keys()},
        {'available', 'user_id', 'name', 'volume', 'id', 'sound_id'},
    )


# ---- available ----

def test__AVAILABLE_CONVERSION__generic():
    """
    Tests whether ``AVAILABLE_CONVERSION`` works as intended.
    """
    # vampytest.assert_is(AVAILABLE_CONVERSION.get_converter, )
    # vampytest.assert_is(AVAILABLE_CONVERSION.put_converter, )
    vampytest.assert_is(AVAILABLE_CONVERSION.validator, validate_available)


def _iter_options__available__get_converter():
    yield True, True
    yield False, False
    yield None, True


@vampytest._(vampytest.call_from(_iter_options__available__get_converter()).returning_last())
def test__AVAILABLE_CONVERSION__get_converter(input_value):
    """
    Tests whether `AVAILABLE_CONVERSION.get_converter` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : `bool`
    """
    return AVAILABLE_CONVERSION.get_converter(input_value)


def _iter_options__available__put_converter():
    yield True, True
    yield False, False


@vampytest._(vampytest.call_from(_iter_options__available__put_converter()).returning_last())
def test__AVAILABLE_CONVERSION__put_converter(input_value):
    """
    Tests whether `AVAILABLE_CONVERSION.put_converter` works as intended.
    
    Parameters
    ----------
    input_value : `bool`
        Processed value.
    
    Returns
    -------
    output : `bool`
    """
    return AVAILABLE_CONVERSION.put_converter(input_value)


# ---- id ----

def test__ID_CONVERSION__generic():
    """
    Tests whether ``ID_CONVERSION`` works as intended.
    """
    vampytest.assert_is(ID_CONVERSION.get_converter, get_converter_id)
    vampytest.assert_is(ID_CONVERSION.put_converter, put_converter_id)
    vampytest.assert_is(ID_CONVERSION.validator, validate_id)


# ---- name ----

def test__NAME_CONVERSION__generic():
    """
    Tests whether ``NAME_CONVERSION`` works as intended.
    """
    vampytest.assert_is(NAME_CONVERSION.get_converter, get_converter_name)
    vampytest.assert_is(NAME_CONVERSION.put_converter, put_converter_name)
    vampytest.assert_is(NAME_CONVERSION.validator, validate_name)


# ---- volume ----

def test__VOLUME_CONVERSION__generic():
    """
    Tests whether ``VOLUME_CONVERSION`` works as intended.
    """
    # vampytest.assert_is(VOLUME_CONVERSION.get_converter, )
    # vampytest.assert_is(VOLUME_CONVERSION.put_converter, )
    vampytest.assert_is(VOLUME_CONVERSION.validator, validate_volume)


def _iter_options__volume__get_converter():
    yield 1.0, 1.0
    yield 0.0, 0.0
    yield None, 1.0


@vampytest._(vampytest.call_from(_iter_options__volume__get_converter()).returning_last())
def test__VOLUME_CONVERSION__get_converter(input_value):
    """
    Tests whether `VOLUME_CONVERSION.get_converter` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : `float`
    """
    return VOLUME_CONVERSION.get_converter(input_value)


def _iter_options__volume__put_converter():
    yield 1.0, 1.0
    yield 0.0, 0.0


@vampytest._(vampytest.call_from(_iter_options__volume__put_converter()).returning_last())
def test__VOLUME_CONVERSION__put_converter(input_value):
    """
    Tests whether `VOLUME_CONVERSION.put_converter` works as intended.
    
    Parameters
    ----------
    input_value : `float`
        Processed value.
    
    Returns
    -------
    output : `float`
    """
    return VOLUME_CONVERSION.put_converter(input_value)


# ---- user_id ----

def test__USER_ID_CONVERSION__generic():
    """
    Tests whether ``USER_ID_CONVERSION`` works as intended.
    """
    vampytest.assert_is(USER_ID_CONVERSION.get_converter, get_converter_id)
    vampytest.assert_is(USER_ID_CONVERSION.put_converter, put_converter_id)
    vampytest.assert_is(USER_ID_CONVERSION.validator, validate_user_id)

