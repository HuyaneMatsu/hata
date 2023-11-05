import vampytest

from ...audit_log_entry_detail_conversion.tests.test__AuditLogEntryDetailConversion import (
    _assert_fields_set as _assert_conversion_fields_set
)
from ...audit_log_entry_detail_conversion.tests.test__AuditLogEntryDetailConversionGroup import (
    _assert_fields_set as _assert_conversion_group_fields_set
)

from ..guild import DAYS_CONVERSION, GUILD_CONVERSIONS, USERS_REMOVED_CONVERSION


def test__GUILD_CONVERSIONS():
    """
    Tests whether `GUILD_CONVERSIONS` contains conversion for every expected key.
    """
    _assert_conversion_group_fields_set(GUILD_CONVERSIONS)
    vampytest.assert_eq(
        {*GUILD_CONVERSIONS.get_converters.keys()},
        {'members_removed', 'delete_member_days'},
    )


# ---- days ----

def test__DAYS_CONVERSION__generic():
    """
    Tests whether ``DAYS_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(DAYS_CONVERSION)
    # vampytest.assert_is(DAYS_CONVERSION.get_converter, )
    # vampytest.assert_is(DAYS_CONVERSION.put_converter, )
    # vampytest.assert_is(DAYS_CONVERSION.validator, )


def _iter_options__days__get_converter():
    days = 123
    yield 0, 0
    yield days, days
    yield None, 0


@vampytest._(vampytest.call_from(_iter_options__days__get_converter()).returning_last())
def test__DAYS_CONVERSION__get_converter(input_value):
    """
    Tests whether `DAYS_CONVERSION.get_converter` works as intended.
    
    Parameters
    ----------
    input_value : `int`
        Raw value.
    
    Returns
    -------
    output : `int`
    """
    return DAYS_CONVERSION.get_converter(input_value)


def _iter_options__days__put_converter():
    days = 123
    yield 0, 0
    yield days, days


@vampytest._(vampytest.call_from(_iter_options__days__put_converter()).returning_last())
def test__DAYS_CONVERSION__put_converter(input_value):
    """
    Tests whether `DAYS_CONVERSION.put_converter` works as intended.
    
    Parameters
    ----------
    input_value : `int`
        Processed value.
    
    Returns
    -------
    output : `int`
    """
    return DAYS_CONVERSION.put_converter(input_value)


def _iter_options__days__validator__passing():
    days = 1123
    yield 0, 0
    yield days, days


def _iter_options__days__validator__type_error():
    yield 12.6


def _iter_options__days__validator__value_error():
    yield -12


@vampytest._(vampytest.call_from(_iter_options__days__validator__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__days__validator__type_error()).raising(TypeError))
@vampytest._(vampytest.call_from(_iter_options__days__validator__value_error()).raising(ValueError))
def test__DAYS_CONVERSION__validator(input_value):
    """
    Tests whether `DAYS_CONVERSION.validator` works as intended.
    
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
    return DAYS_CONVERSION.validator(input_value)


# ---- users_removed ----

def test__USERS_REMOVED_CONVERSION__generic():
    """
    Tests whether ``USERS_REMOVED_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(USERS_REMOVED_CONVERSION)
    # vampytest.assert_is(USERS_REMOVED_CONVERSION.get_converter, )
    # vampytest.assert_is(USERS_REMOVED_CONVERSION.put_converter, )
    # vampytest.assert_is(USERS_REMOVED_CONVERSION.validator, )


def _iter_options__users_removed__get_converter():
    users_removed = 123
    yield 0, 0
    yield users_removed, users_removed
    yield None, 0


@vampytest._(vampytest.call_from(_iter_options__users_removed__get_converter()).returning_last())
def test__USERS_REMOVED_CONVERSION__get_converter(input_value):
    """
    Tests whether `USERS_REMOVED_CONVERSION.get_converter` works as intended.
    
    Parameters
    ----------
    input_value : `int`
        Raw value.
    
    Returns
    -------
    output : `int`
    """
    return USERS_REMOVED_CONVERSION.get_converter(input_value)


def _iter_options__users_removed__put_converter():
    users_removed = 123
    yield 0, 0
    yield users_removed, users_removed


@vampytest._(vampytest.call_from(_iter_options__users_removed__put_converter()).returning_last())
def test__USERS_REMOVED_CONVERSION__put_converter(input_value):
    """
    Tests whether `USERS_REMOVED_CONVERSION.put_converter` works as intended.
    
    Parameters
    ----------
    input_value : `int`
        Processed value.
    
    Returns
    -------
    output : `int`
    """
    return USERS_REMOVED_CONVERSION.put_converter(input_value)


def _iter_options__users_removed__validator__passing():
    users_removed = 1123
    yield 0, 0
    yield users_removed, users_removed


def _iter_options__users_removed__validator__type_error():
    yield 12.6


def _iter_options__users_removed__validator__value_error():
    yield -12


@vampytest._(vampytest.call_from(_iter_options__users_removed__validator__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__users_removed__validator__type_error()).raising(TypeError))
@vampytest._(vampytest.call_from(_iter_options__users_removed__validator__value_error()).raising(ValueError))
def test__USERS_REMOVED_CONVERSION__validator(input_value):
    """
    Tests whether `USERS_REMOVED_CONVERSION.validator` works as intended.
    
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
    return USERS_REMOVED_CONVERSION.validator(input_value)
