import vampytest

from ....scheduled_event import PrivacyLevel
from ....stage.stage.fields import validate_privacy_level, validate_topic

from ...conversion_helpers.converters import get_converter_description, put_converter_description

from ..stage import PRIVACY_LEVEL_CONVERSION, STAGE_CONVERSIONS, TOPIC_CONVERSION


def test__STAGE_CONVERSIONS():
    """
    Tests whether `STAGE_CONVERSIONS` contains conversion for every expected key.
    """
    vampytest.assert_eq(
        {*STAGE_CONVERSIONS.get_converters.keys()},
        {'privacy_level', 'topic'},
    )


# ---- privacy_level ----

def test__PRIVACY_LEVEL_CONVERSION__generic():
    """
    Tests whether ``PRIVACY_LEVEL_CONVERSION`` works as intended.
    """
    # vampytest.assert_is(PRIVACY_LEVEL_CONVERSION.get_converter, )
    # vampytest.assert_is(PRIVACY_LEVEL_CONVERSION.put_converter, )
    vampytest.assert_is(PRIVACY_LEVEL_CONVERSION.validator, validate_privacy_level)


def _iter_options__privacy_level__get_converter():
    yield None, PrivacyLevel.none
    yield PrivacyLevel.public.value, PrivacyLevel.public


@vampytest._(vampytest.call_from(_iter_options__privacy_level__get_converter()).returning_last())
def test__PRIVACY_LEVEL_CONVERSION__get_converter(input_value):
    """
    Tests whether `PRIVACY_LEVEL_CONVERSION.get_converter` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : ``PrivacyLevel``
    """
    return PRIVACY_LEVEL_CONVERSION.get_converter(input_value)


def _iter_options__privacy_level__put_converter():
    yield PrivacyLevel.none, PrivacyLevel.none.value
    yield PrivacyLevel.public, PrivacyLevel.public.value


@vampytest._(vampytest.call_from(_iter_options__privacy_level__put_converter()).returning_last())
def test__PRIVACY_LEVEL_CONVERSION__put_converter(input_value):
    """
    Tests whether `PRIVACY_LEVEL_CONVERSION.put_converter` works as intended.
    
    Parameters
    ----------
    input_value : ``PrivacyLevel``
        Processed value.
    
    Returns
    -------
    output : `int`
    """
    return PRIVACY_LEVEL_CONVERSION.put_converter(input_value)


# ---- topic ----

def test__TOPIC_CONVERSION__generic():
    """
    Tests whether ``TOPIC_CONVERSION`` works as intended.
    """
    vampytest.assert_is(TOPIC_CONVERSION.get_converter, get_converter_description)
    vampytest.assert_is(TOPIC_CONVERSION.put_converter, put_converter_description)
    vampytest.assert_is(TOPIC_CONVERSION.validator, validate_topic)
