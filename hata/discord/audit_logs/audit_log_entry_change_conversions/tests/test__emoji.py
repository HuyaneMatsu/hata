import vampytest

from ....emoji.emoji.fields import validate_available, validate_name, validate_role_ids

from ...audit_log_entry_change_conversion.tests.test__AuditLogEntryChangeConversion import (
    _assert_fields_set as _assert_conversion_fields_set
)
from ...audit_log_entry_change_conversion.tests.test__AuditLogEntryChangeConversionGroup import (
    _assert_fields_set as _assert_conversion_group_fields_set
)
from ...conversion_helpers.converters import (
    get_converter_ids, get_converter_name, put_converter_ids, put_converter_name
)

from ..emoji import AVAILABLE_CONVERSION, EMOJI_CONVERSIONS, NAME_CONVERSION, ROLE_IDS_CONVERSION


def test__EMOJI_CONVERSIONS():
    """
    Tests whether `EMOJI_CONVERSIONS` contains conversion for every expected key.
    """
    _assert_conversion_group_fields_set(EMOJI_CONVERSIONS)
    vampytest.assert_eq(
        {*EMOJI_CONVERSIONS.get_converters.keys()},
        {'available', 'name', 'roles'},
    )

# ---- available ----

def test__AVAILABLE_CONVERSION__generic():
    """
    Tests whether ``AVAILABLE_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(AVAILABLE_CONVERSION)
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


# ---- name ----

def test__NAME_CONVERSION__generic():
    """
    Tests whether ``NAME_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(NAME_CONVERSION)
    vampytest.assert_is(NAME_CONVERSION.get_converter, get_converter_name)
    vampytest.assert_is(NAME_CONVERSION.put_converter, put_converter_name)
    vampytest.assert_is(NAME_CONVERSION.validator, validate_name)


# ---- role_ids ----

def test__ROLE_IDS_CONVERSION__generic():
    """
    Tests whether ``ROLE_IDS_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(ROLE_IDS_CONVERSION)
    vampytest.assert_is(ROLE_IDS_CONVERSION.get_converter, get_converter_ids)
    vampytest.assert_is(ROLE_IDS_CONVERSION.put_converter, put_converter_ids)
    vampytest.assert_is(ROLE_IDS_CONVERSION.validator, validate_role_ids)

