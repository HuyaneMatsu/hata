import vampytest

from ....channel import PermissionOverwriteTargetType
from ....channel.permission_overwrite.fields import validate_target_id, validate_target_type
from ....role.role.fields import validate_name

from ...audit_log_entry_detail_conversion.tests.test__AuditLogEntryDetailConversion import (
    _assert_fields_set as _assert_conversion_fields_set
)
from ...audit_log_entry_detail_conversion.tests.test__AuditLogEntryDetailConversionGroup import (
    _assert_fields_set as _assert_conversion_group_fields_set
)
from ...conversion_helpers.converters import (
    value_deserializer_id, value_deserializer_name, value_serializer_id, value_serializer_name
)

from ..channel_permission_overwrite import (
    CHANNEL_PERMISSION_OVERWRITE_CONVERSIONS, ROLE_NAME_CONVERSION, TARGET_ID_CONVERSION, TARGET_TYPE_CONVERSION
)


def test__APPLICATION_COMMAND_CONVERSIONS():
    """
    Tests whether `CHANNEL_PERMISSION_OVERWRITE_CONVERSIONS` contains conversion for every expected key.
    """
    _assert_conversion_group_fields_set(CHANNEL_PERMISSION_OVERWRITE_CONVERSIONS)
    vampytest.assert_eq(
        {conversion.field_key for conversion in CHANNEL_PERMISSION_OVERWRITE_CONVERSIONS.conversions},
        {'id', 'role_name', 'type'},
    )


# ---- role_name ----

def test__ROLE_NAME_CONVERSION__generic():
    """
    Tests whether ``ROLE_NAME_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(ROLE_NAME_CONVERSION)
    vampytest.assert_is(ROLE_NAME_CONVERSION.value_deserializer, value_deserializer_name)
    vampytest.assert_is(ROLE_NAME_CONVERSION.value_serializer, value_serializer_name)
    vampytest.assert_is(ROLE_NAME_CONVERSION.value_validator, validate_name)


# ---- target_id ----

def test__TARGET_ID_CONVERSION__generic():
    """
    Tests whether ``TARGET_ID_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(TARGET_ID_CONVERSION)
    vampytest.assert_is(TARGET_ID_CONVERSION.value_deserializer, value_deserializer_id)
    vampytest.assert_is(TARGET_ID_CONVERSION.value_serializer, value_serializer_id)
    vampytest.assert_is(TARGET_ID_CONVERSION.value_validator, validate_target_id)


# ---- target_type ----

def test__TARGET_TYPE_CONVERSION__generic():
    """
    Tests whether ``TARGET_TYPE_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(TARGET_TYPE_CONVERSION)
    # vampytest.assert_is(TARGET_TYPE_CONVERSION.value_deserializer, )
    # vampytest.assert_is(TARGET_TYPE_CONVERSION.value_serializer, )
    vampytest.assert_is(TARGET_TYPE_CONVERSION.value_validator, validate_target_type)


def _iter_options__target_type__value_deserializer():
    yield None, PermissionOverwriteTargetType.role
    yield str(PermissionOverwriteTargetType.user.value), PermissionOverwriteTargetType.user
    yield PermissionOverwriteTargetType.user.value, PermissionOverwriteTargetType.user


@vampytest._(vampytest.call_from(_iter_options__target_type__value_deserializer()).returning_last())
def test__TARGET_TYPE_CONVERSION__value_deserializer(input_value):
    """
    Tests whether `TARGET_TYPE_CONVERSION.value_deserializer` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : ``PermissionOverwriteTargetType``
    """
    return TARGET_TYPE_CONVERSION.value_deserializer(input_value)


def _iter_options__target_type__value_serializer():
    yield PermissionOverwriteTargetType.role, str(PermissionOverwriteTargetType.role.value)
    yield PermissionOverwriteTargetType.user, str(PermissionOverwriteTargetType.user.value)


@vampytest._(vampytest.call_from(_iter_options__target_type__value_serializer()).returning_last())
def test__TARGET_TYPE_CONVERSION__value_serializer(input_value):
    """
    Tests whether `TARGET_TYPE_CONVERSION.value_serializer` works as intended.
    
    Parameters
    ----------
    input_value : ``PermissionOverwriteTargetType``
        Processed value.
    
    Returns
    -------
    output : `str`
    """
    return TARGET_TYPE_CONVERSION.value_serializer(input_value)
