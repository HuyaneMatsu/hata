import vampytest

from ....invite.invite.fields import (
    validate_channel_id, validate_code, validate_max_age, validate_max_uses, validate_temporary
)

from ...audit_log_entry_change_conversion import AuditLogEntryChangeConversion
from ...conversion_helpers.converters import get_converter_id, get_converter_name, put_converter_id, put_converter_name

from ..invite import (
    CHANNEL_ID_CONVERSION, CODE_CONVERSION, INVITE_CONVERSIONS, MAX_AGE_CONVERSION, MAX_USES_CONVERSION,
    TEMPORARY_CONVERSION
)


def test__INVITE_CONVERSIONS():
    """
    Tests whether `INVITE_CONVERSIONS` contains conversion for every expected key.
    """
    vampytest.assert_eq(
        {*INVITE_CONVERSIONS.get_converters.keys()},
        {'channel_id', 'code', 'max_age', 'max_uses', 'temporary'},
    )


# ---- channel_id ----

def test__CHANNEL_ID_CONVERSION__generic():
    """
    Tests whether ``CHANNEL_ID_CONVERSION`` works as intended.
    """
    vampytest.assert_is(CHANNEL_ID_CONVERSION.get_converter, get_converter_id)
    vampytest.assert_is(CHANNEL_ID_CONVERSION.put_converter, put_converter_id)
    vampytest.assert_is(CHANNEL_ID_CONVERSION.validator, validate_channel_id)


# ---- code ----

def test__CODE_CONVERSION__generic():
    """
    Tests whether ``CODE_CONVERSION`` works as intended.
    """
    vampytest.assert_is(CODE_CONVERSION.get_converter, get_converter_name)
    vampytest.assert_is(CODE_CONVERSION.put_converter, put_converter_name)
    vampytest.assert_is(CODE_CONVERSION.validator, validate_code)


# ---- max_age ----

def test__MAX_AGE_CONVERSION__generic():
    """
    Tests whether ``MAX_AGE_CONVERSION`` works as intended.
    """
    # vampytest.assert_is(MAX_AGE_CONVERSION.get_converter, )
    # vampytest.assert_is(MAX_AGE_CONVERSION.put_converter, )
    vampytest.assert_is(MAX_AGE_CONVERSION.validator, validate_max_age)


# ---- max_uses ----

def test__MAX_USES_CONVERSION__generic():
    """
    Tests whether ``MAX_USES_CONVERSION`` works as intended.
    """
    # vampytest.assert_is(MAX_USES_CONVERSION.get_converter, )
    # vampytest.assert_is(MAX_USES_CONVERSION.put_converter, )
    vampytest.assert_is(MAX_USES_CONVERSION.validator, validate_max_uses)


# ----

def _iter_options__max_x__get_converter():
    yield MAX_AGE_CONVERSION, 60, 60
    yield MAX_AGE_CONVERSION, 0, 0
    yield MAX_AGE_CONVERSION, None, 0
    yield MAX_USES_CONVERSION, 60, 60
    yield MAX_USES_CONVERSION, 0, 0
    yield MAX_USES_CONVERSION, None, 0


@vampytest._(vampytest.call_from(_iter_options__max_x__get_converter()).returning_last())
def test__MAX_X_CONVERSION__get_converter(conversion, input_value):
    """
    Tests whether `MAX_AGE_CONVERSION.get_converter` and `MAX_USES_CONVERSION.get_converter` works as intended.
    
    Parameters
    ----------
    conversion : ``AuditLogEntryChangeConversion``
        Conversion to test.
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : `int`
    """
    return conversion.get_converter(input_value)


def _iter_options__max_x__put_converter():
    yield MAX_AGE_CONVERSION, 60, 60
    yield MAX_AGE_CONVERSION, 0, 0
    yield MAX_USES_CONVERSION, 60, 60
    yield MAX_USES_CONVERSION, 0, 0


@vampytest._(vampytest.call_from(_iter_options__max_x__put_converter()).returning_last())
def test__MAX_X_CONVERSION__put_converter(conversion, input_value):
    """
    Tests whether `MAX_AGE_CONVERSION.put_converter` and `MAX_AGE_CONVERSION.put_converter` works as intended.
    
    Parameters
    ----------
    conversion : ``AuditLogEntryChangeConversion``
        Conversion to test.
    input_value : `int`
        Processed value.
    
    Returns
    -------
    output : `int`
    """
    return conversion.put_converter(input_value)


# ---- temporary ----

def test__TEMPORARY_CONVERSION__generic():
    """
    Tests whether ``TEMPORARY_CONVERSION`` works as intended.
    """
    # vampytest.assert_is(TEMPORARY_CONVERSION.get_converter, )
    # vampytest.assert_is(TEMPORARY_CONVERSION.put_converter, )
    vampytest.assert_is(TEMPORARY_CONVERSION.validator, validate_temporary)


def _iter_options__temporary__get_converter():
    yield True, True
    yield False, False
    yield None, False


@vampytest._(vampytest.call_from(_iter_options__temporary__get_converter()).returning_last())
def test__TEMPORARY_CONVERSION__get_converter(input_value):
    """
    Tests whether `TEMPORARY_CONVERSION.get_converter` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : `bool`
    """
    return TEMPORARY_CONVERSION.get_converter(input_value)


def _iter_options__temporary__put_converter():
    yield True, True
    yield False, False


@vampytest._(vampytest.call_from(_iter_options__temporary__put_converter()).returning_last())
def test__TEMPORARY_CONVERSION__put_converter(input_value):
    """
    Tests whether `TEMPORARY_CONVERSION.put_converter` works as intended.
    
    Parameters
    ----------
    input_value : `bool`
        Processed value.
    
    Returns
    -------
    output : `bool`
    """
    return TEMPORARY_CONVERSION.put_converter(input_value)
