import vampytest

from ....invite import InviteFlag
from ....invite.invite.fields import (
    validate_channel_id, validate_code, validate_flags, validate_inviter_id, validate_max_age, validate_max_uses,
    validate_temporary, validate_uses
)

from ...audit_log_entry_change_conversion import AuditLogEntryChangeConversion
from ...audit_log_entry_change_conversion.tests.test__AuditLogEntryChangeConversion import (
    _assert_fields_set as _assert_conversion_fields_set
)
from ...audit_log_entry_change_conversion.tests.test__AuditLogEntryChangeConversionGroup import (
    _assert_fields_set as _assert_conversion_group_fields_set
)
from ...conversion_helpers.converters import get_converter_id, get_converter_name, put_converter_id, put_converter_name

from ..invite import (
    CHANNEL_ID_CONVERSION, CODE_CONVERSION, FLAGS_CONVERSION, INVITE_CONVERSIONS, INVITER_ID_CONVERSION,
    MAX_AGE_CONVERSION, MAX_USES_CONVERSION, TEMPORARY_CONVERSION, USES_CONVERSION
)


def test__INVITE_CONVERSIONS():
    """
    Tests whether `INVITE_CONVERSIONS` contains conversion for every expected key.
    """
    _assert_conversion_group_fields_set(INVITE_CONVERSIONS)
    vampytest.assert_eq(
        {*INVITE_CONVERSIONS.get_converters.keys()},
        {'uses', 'inviter_id', 'channel_id', 'flags', 'code', 'max_age', 'max_uses', 'temporary'},
    )


# ---- channel_id ----

def test__CHANNEL_ID_CONVERSION__generic():
    """
    Tests whether ``CHANNEL_ID_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(CHANNEL_ID_CONVERSION)
    vampytest.assert_is(CHANNEL_ID_CONVERSION.get_converter, get_converter_id)
    vampytest.assert_is(CHANNEL_ID_CONVERSION.put_converter, put_converter_id)
    vampytest.assert_is(CHANNEL_ID_CONVERSION.validator, validate_channel_id)


# ---- code ----

def test__CODE_CONVERSION__generic():
    """
    Tests whether ``CODE_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(CODE_CONVERSION)
    vampytest.assert_is(CODE_CONVERSION.get_converter, get_converter_name)
    vampytest.assert_is(CODE_CONVERSION.put_converter, put_converter_name)
    vampytest.assert_is(CODE_CONVERSION.validator, validate_code)


# ---- flags ----

def test__FLAGS_CONVERSION__generic():
    """
    Tests whether ``FLAGS_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(FLAGS_CONVERSION)
    # vampytest.assert_is(FLAGS_CONVERSION.get_converter, )
    # vampytest.assert_is(FLAGS_CONVERSION.put_converter, )
    vampytest.assert_is(FLAGS_CONVERSION.validator, validate_flags)


def _iter_options__flags__get_converter():
    yield 60, InviteFlag(60)
    yield 0, InviteFlag()
    yield None, InviteFlag()


@vampytest._(vampytest.call_from(_iter_options__flags__get_converter()).returning_last())
def test__FLAGS_CONVERSION__get_converter(input_value):
    """
    Tests whether `FLAGS_CONVERSION.get_converter` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : ``InviteFlag``
    """
    output = FLAGS_CONVERSION.get_converter(input_value)
    vampytest.assert_instance(output, InviteFlag)
    return output


def _iter_options__flags__put_converter():
    yield InviteFlag(60), 60
    yield InviteFlag(), 0


@vampytest._(vampytest.call_from(_iter_options__flags__put_converter()).returning_last())
def test__FLAGS_CONVERSION__put_converter(input_value):
    """
    Tests whether `FLAGS_CONVERSION.put_converter` works as intended.
    
    Parameters
    ----------
    input_value : ``InviteFlag``
        Processed value.
    
    Returns
    -------
    output : `int`
    """
    output = FLAGS_CONVERSION.put_converter(input_value)
    vampytest.assert_instance(output, int, accept_subtypes = False)
    return output


# ---- inviter_id ----

def test__INVITER_ID_CONVERSION__generic():
    """
    Tests whether ``INVITER_ID_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(INVITER_ID_CONVERSION)
    vampytest.assert_is(INVITER_ID_CONVERSION.get_converter, get_converter_id)
    vampytest.assert_is(INVITER_ID_CONVERSION.put_converter, put_converter_id)
    vampytest.assert_is(INVITER_ID_CONVERSION.validator, validate_inviter_id)


# ---- max_age ----

def test__MAX_AGE_CONVERSION__generic():
    """
    Tests whether ``MAX_AGE_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(MAX_AGE_CONVERSION)
    # vampytest.assert_is(MAX_AGE_CONVERSION.get_converter, )
    # vampytest.assert_is(MAX_AGE_CONVERSION.put_converter, )
    vampytest.assert_is(MAX_AGE_CONVERSION.validator, validate_max_age)


# ---- max_uses ----

def test__MAX_USES_CONVERSION__generic():
    """
    Tests whether ``MAX_USES_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(MAX_USES_CONVERSION)
    # vampytest.assert_is(MAX_USES_CONVERSION.get_converter, )
    # vampytest.assert_is(MAX_USES_CONVERSION.put_converter, )
    vampytest.assert_is(MAX_USES_CONVERSION.validator, validate_max_uses)


# ---- uses ----

def test__USES_CONVERSION__generic():
    """
    Tests whether ``USES_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(USES_CONVERSION)
    # vampytest.assert_is(USES_CONVERSION.get_converter, )
    # vampytest.assert_is(USES_CONVERSION.put_converter, )
    vampytest.assert_is(USES_CONVERSION.validator, validate_uses)


# ----

def _iter_options__max_x__get_converter():
    yield MAX_AGE_CONVERSION, 60, 60
    yield MAX_AGE_CONVERSION, 0, 0
    yield MAX_AGE_CONVERSION, None, 0
    yield MAX_USES_CONVERSION, 60, 60
    yield MAX_USES_CONVERSION, 0, 0
    yield MAX_USES_CONVERSION, None, 0
    yield USES_CONVERSION, 60, 60
    yield USES_CONVERSION, 0, 0
    yield USES_CONVERSION, None, 0


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
    yield USES_CONVERSION, 60, 60
    yield USES_CONVERSION, 0, 0


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
    _assert_conversion_fields_set(TEMPORARY_CONVERSION)
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
