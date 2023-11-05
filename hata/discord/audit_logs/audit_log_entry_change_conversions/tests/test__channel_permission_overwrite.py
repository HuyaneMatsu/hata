import vampytest

from ....channel import PermissionOverwriteTargetType
from ....channel.permission_overwrite.fields import (
    validate_allow, validate_deny, validate_target_id, validate_target_type
)
from ....permission import Permission
from ....permission.constants import PERMISSION_ALLOW_KEY, PERMISSION_DENY_KEY

from ...audit_log_entry_change_conversion.tests.test__AuditLogEntryChangeConversion import (
    _assert_fields_set as _assert_conversion_fields_set
)
from ...audit_log_entry_change_conversion.tests.test__AuditLogEntryChangeConversionGroup import (
    _assert_fields_set as _assert_conversion_group_fields_set
)
from ...conversion_helpers.converters import get_converter_id, put_converter_id

from ..channel_permission_overwrite import (
    ALLOW_CONVERSION, CHANNEL_PERMISSION_OVERWRITE_CONVERSIONS, DENY_CONVERSION, TARGET_ID_CONVERSION,
    TARGET_TYPE_CONVERSION
)


def test__APPLICATION_COMMAND_CONVERSIONS():
    """
    Tests whether `CHANNEL_PERMISSION_OVERWRITE_CONVERSIONS` contains conversion for every expected key.
    """
    _assert_conversion_group_fields_set(CHANNEL_PERMISSION_OVERWRITE_CONVERSIONS)
    vampytest.assert_eq(
        {*CHANNEL_PERMISSION_OVERWRITE_CONVERSIONS.get_converters.keys()},
        {PERMISSION_ALLOW_KEY, PERMISSION_DENY_KEY, 'id', 'type'},
    )

# ---- allow ----

def test__ALLOW_CONVERSION__generic():
    """
    Tests whether ``ALLOW_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(ALLOW_CONVERSION)
    # vampytest.assert_is(ALLOW_CONVERSION.get_converter, )
    # vampytest.assert_is(ALLOW_CONVERSION.put_converter, )
    vampytest.assert_is(ALLOW_CONVERSION.validator, validate_allow)


# ---- deny ----

def test__DENY_CONVERSION__generic():
    """
    Tests whether ``DENY_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(DENY_CONVERSION)
    # vampytest.assert_is(DENY_CONVERSION.get_converter, )
    # vampytest.assert_is(DENY_CONVERSION.put_converter, )
    vampytest.assert_is(DENY_CONVERSION.validator, validate_deny)


# ----

def _iter_options__permission__get_converter():
    yield ALLOW_CONVERSION, '60', Permission(60)
    yield ALLOW_CONVERSION, '0', Permission()
    yield ALLOW_CONVERSION, None, Permission()
    yield DENY_CONVERSION, '60', Permission(60)
    yield DENY_CONVERSION, '0', Permission()
    yield DENY_CONVERSION, None, Permission()


@vampytest._(vampytest.call_from(_iter_options__permission__get_converter()).returning_last())
def test__permission_conversions__get_converter(conversion, input_value):
    """
    Tests whether `permission_conversions.get_converter` works as intended.
    
    Parameters
    ----------
    conversion : ``AuditLogEntryChangeConversion``
        Conversion to use.
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : ``Permission``
    """
    output = conversion.get_converter(input_value)
    vampytest.assert_instance(output, Permission)
    return output


def _iter_options__permission__put_converter():
    yield ALLOW_CONVERSION, Permission(60), '60'
    yield ALLOW_CONVERSION, Permission(), '0'
    yield DENY_CONVERSION, Permission(60), '60'
    yield DENY_CONVERSION, Permission(), '0'


@vampytest._(vampytest.call_from(_iter_options__permission__put_converter()).returning_last())
def test__permission_conversions__put_converter(conversion, input_value):
    """
    Tests whether `permission_conversions.put_converter` works as intended.
    
    Parameters
    ----------
    conversion : ``AuditLogEntryChangeConversion``
        Conversion to use.
    input_value : ``Permission``
        Processed value.
    
    Returns
    -------
    output : `str`
    """
    output = conversion.put_converter(input_value)
    vampytest.assert_instance(output, str)
    return output


# ---- target_id ----

def test__TARGET_ID_CONVERSION__generic():
    """
    Tests whether ``TARGET_ID_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(TARGET_ID_CONVERSION)
    vampytest.assert_is(TARGET_ID_CONVERSION.get_converter, get_converter_id)
    vampytest.assert_is(TARGET_ID_CONVERSION.put_converter, put_converter_id)
    vampytest.assert_is(TARGET_ID_CONVERSION.validator, validate_target_id)


# ---- target_type ----

def test__TARGET_TYPE_CONVERSION__generic():
    """
    Tests whether ``TARGET_TYPE_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(TARGET_TYPE_CONVERSION)
    # vampytest.assert_is(TARGET_TYPE_CONVERSION.get_converter, )
    # vampytest.assert_is(TARGET_TYPE_CONVERSION.put_converter, )
    vampytest.assert_is(TARGET_TYPE_CONVERSION.validator, validate_target_type)


def _iter_options__target_type__get_converter():
    yield None, PermissionOverwriteTargetType.role
    yield str(PermissionOverwriteTargetType.user.value), PermissionOverwriteTargetType.user
    yield PermissionOverwriteTargetType.user.value, PermissionOverwriteTargetType.user


@vampytest._(vampytest.call_from(_iter_options__target_type__get_converter()).returning_last())
def test__TARGET_TYPE_CONVERSION__get_converter(input_value):
    """
    Tests whether `TARGET_TYPE_CONVERSION.get_converter` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : ``PermissionOverwriteTargetType``
    """
    return TARGET_TYPE_CONVERSION.get_converter(input_value)


def _iter_options__target_type__put_converter():
    yield PermissionOverwriteTargetType.role, str(PermissionOverwriteTargetType.role.value)
    yield PermissionOverwriteTargetType.user, str(PermissionOverwriteTargetType.user.value)


@vampytest._(vampytest.call_from(_iter_options__target_type__put_converter()).returning_last())
def test__TARGET_TYPE_CONVERSION__put_converter(input_value):
    """
    Tests whether `TARGET_TYPE_CONVERSION.put_converter` works as intended.
    
    Parameters
    ----------
    input_value : ``PermissionOverwriteTargetType``
        Processed value.
    
    Returns
    -------
    output : `str`
    """
    return TARGET_TYPE_CONVERSION.put_converter(input_value)
