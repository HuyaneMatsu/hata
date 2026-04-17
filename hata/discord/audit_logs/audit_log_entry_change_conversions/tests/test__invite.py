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
from ...conversion_helpers.converters import value_deserializer_id, value_deserializer_name, value_serializer_id, value_serializer_name

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
        {*INVITE_CONVERSIONS.iter_field_keys()},
        {'uses', 'inviter_id', 'channel_id', 'flags', 'code', 'max_age', 'max_uses', 'temporary'},
    )


# ---- channel_id ----

def test__CHANNEL_ID_CONVERSION__generic():
    """
    Tests whether ``CHANNEL_ID_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(CHANNEL_ID_CONVERSION)
    vampytest.assert_is(CHANNEL_ID_CONVERSION.value_deserializer, value_deserializer_id)
    vampytest.assert_is(CHANNEL_ID_CONVERSION.value_serializer, value_serializer_id)
    vampytest.assert_is(CHANNEL_ID_CONVERSION.value_validator, validate_channel_id)


# ---- code ----

def test__CODE_CONVERSION__generic():
    """
    Tests whether ``CODE_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(CODE_CONVERSION)
    vampytest.assert_is(CODE_CONVERSION.value_deserializer, value_deserializer_name)
    vampytest.assert_is(CODE_CONVERSION.value_serializer, value_serializer_name)
    vampytest.assert_is(CODE_CONVERSION.value_validator, validate_code)


# ---- flags ----

def test__FLAGS_CONVERSION__generic():
    """
    Tests whether ``FLAGS_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(FLAGS_CONVERSION)
    vampytest.assert_is(FLAGS_CONVERSION.value_validator, validate_flags)


def _iter_options__flags__value_deserializer():
    yield 60, InviteFlag(60)
    yield 0, InviteFlag()
    yield None, InviteFlag()


@vampytest._(vampytest.call_from(_iter_options__flags__value_deserializer()).returning_last())
def test__FLAGS_CONVERSION__value_deserializer(input_value):
    """
    Tests whether `FLAGS_CONVERSION.value_deserializer` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : ``InviteFlag``
    """
    output = FLAGS_CONVERSION.value_deserializer(input_value)
    vampytest.assert_instance(output, InviteFlag)
    return output


def _iter_options__flags__value_serializer():
    yield InviteFlag(60), 60
    yield InviteFlag(), 0


@vampytest._(vampytest.call_from(_iter_options__flags__value_serializer()).returning_last())
def test__FLAGS_CONVERSION__value_serializer(input_value):
    """
    Tests whether `FLAGS_CONVERSION.value_serializer` works as intended.
    
    Parameters
    ----------
    input_value : ``InviteFlag``
        Processed value.
    
    Returns
    -------
    output : `int`
    """
    output = FLAGS_CONVERSION.value_serializer(input_value)
    vampytest.assert_instance(output, int, accept_subtypes = False)
    return output


# ---- inviter_id ----

def test__INVITER_ID_CONVERSION__generic():
    """
    Tests whether ``INVITER_ID_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(INVITER_ID_CONVERSION)
    vampytest.assert_is(INVITER_ID_CONVERSION.value_deserializer, value_deserializer_id)
    vampytest.assert_is(INVITER_ID_CONVERSION.value_serializer, value_serializer_id)
    vampytest.assert_is(INVITER_ID_CONVERSION.value_validator, validate_inviter_id)


# ---- max_age ----

def test__MAX_AGE_CONVERSION__generic():
    """
    Tests whether ``MAX_AGE_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(MAX_AGE_CONVERSION)
    vampytest.assert_is(MAX_AGE_CONVERSION.value_serializer, None)
    vampytest.assert_is(MAX_AGE_CONVERSION.value_validator, validate_max_age)


# ---- max_uses ----

def test__MAX_USES_CONVERSION__generic():
    """
    Tests whether ``MAX_USES_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(MAX_USES_CONVERSION)
    vampytest.assert_is(MAX_USES_CONVERSION.value_serializer, None)
    vampytest.assert_is(MAX_USES_CONVERSION.value_validator, validate_max_uses)


# ---- uses ----

def test__USES_CONVERSION__generic():
    """
    Tests whether ``USES_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(USES_CONVERSION)
    vampytest.assert_is(USES_CONVERSION.value_serializer, None)
    vampytest.assert_is(USES_CONVERSION.value_validator, validate_uses)


# ----

def _iter_options__max_x__value_deserializer():
    yield MAX_AGE_CONVERSION, 60, 60
    yield MAX_AGE_CONVERSION, 0, 0
    yield MAX_AGE_CONVERSION, None, 0
    yield MAX_USES_CONVERSION, 60, 60
    yield MAX_USES_CONVERSION, 0, 0
    yield MAX_USES_CONVERSION, None, 0
    yield USES_CONVERSION, 60, 60
    yield USES_CONVERSION, 0, 0
    yield USES_CONVERSION, None, 0


@vampytest._(vampytest.call_from(_iter_options__max_x__value_deserializer()).returning_last())
def test__MAX_X_CONVERSION__value_deserializer(conversion, input_value):
    """
    Tests whether `MAX_AGE_CONVERSION.value_deserializer` and `MAX_USES_CONVERSION.value_deserializer` works as intended.
    
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
    return conversion.value_deserializer(input_value)


# ---- temporary ----

def test__TEMPORARY_CONVERSION__generic():
    """
    Tests whether ``TEMPORARY_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(TEMPORARY_CONVERSION)
    vampytest.assert_is(TEMPORARY_CONVERSION.value_serializer, None)
    vampytest.assert_is(TEMPORARY_CONVERSION.value_validator, validate_temporary)


def _iter_options__temporary__value_deserializer():
    yield True, True
    yield False, False
    yield None, False


@vampytest._(vampytest.call_from(_iter_options__temporary__value_deserializer()).returning_last())
def test__TEMPORARY_CONVERSION__value_deserializer(input_value):
    """
    Tests whether `TEMPORARY_CONVERSION.value_deserializer` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : `bool`
    """
    return TEMPORARY_CONVERSION.value_deserializer(input_value)
