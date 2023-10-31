import vampytest

from ....core import BUILTIN_EMOJIS
from ....emoji import put_exclusive_emoji_data_into
from ....soundboard.soundboard_sound.fields import validate_available, validate_emoji, validate_name, validate_volume

from ...conversion_helpers.converters import get_converter_name, put_converter_name

from ..soundboard_sound import (
    AVAILABLE_CONVERSION, EMOJI_CONVERSION, NAME_CONVERSION, SOUNDBOARD_SOUND_CONVERSIONS, VOLUME_CONVERSION
)


def test__SOUNDBOARD_SOUND_CONVERSIONS():
    """
    Tests whether `SOUNDBOARD_SOUND_CONVERSIONS` contains conversion for every expected key.
    """
    vampytest.assert_eq(
        {*SOUNDBOARD_SOUND_CONVERSIONS.get_converters.keys()},
        {'available', 'emoji', 'name', 'volume'},
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


# ---- emoji ----

def test__EMOJI_CONVERSION__generic():
    """
    Tests whether ``EMOJI_CONVERSION`` works as intended.
    """
    # vampytest.assert_is(EMOJI_CONVERSION.get_converter, )
    # vampytest.assert_is(EMOJI_CONVERSION.put_converter, )
    vampytest.assert_is(EMOJI_CONVERSION.validator, validate_emoji)


def _iter_options__emoji__get_converter():
    emoji = BUILTIN_EMOJIS['x']
    yield None, None
    yield put_exclusive_emoji_data_into(emoji, {}), emoji


@vampytest._(vampytest.call_from(_iter_options__emoji__get_converter()).returning_last())
def test__EMOJI_CONVERSION__get_converter(input_value):
    """
    Tests whether `EMOJI_CONVERSION.get_converter` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : `None | Emoji`
    """
    return EMOJI_CONVERSION.get_converter(input_value)


def _iter_options__emoji__put_converter():
    emoji = BUILTIN_EMOJIS['x']
    yield None, None
    yield emoji, put_exclusive_emoji_data_into(emoji, {})


@vampytest._(vampytest.call_from(_iter_options__emoji__put_converter()).returning_last())
def test__EMOJI_CONVERSION__put_converter(input_value):
    """
    Tests whether `EMOJI_CONVERSION.put_converter` works as intended.
    
    Parameters
    ----------
    input_value : `None | Emoji`
        Processed value.
    
    Returns
    -------
    output : `None | dict<str, object>`
    """
    return EMOJI_CONVERSION.put_converter(input_value)


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
