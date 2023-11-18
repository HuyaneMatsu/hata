import vampytest

from ....application_command.application_command_permission.fields import validate_application_id, validate_guild_id
from ....application_command.application_command_permission_overwrite.fields import validate_channel_id

from ...audit_log_entry_detail_conversion.tests.test__AuditLogEntryDetailConversion import (
    _assert_fields_set as _assert_conversion_fields_set
)
from ...audit_log_entry_detail_conversion.tests.test__AuditLogEntryDetailConversionGroup import (
    _assert_fields_set as _assert_conversion_group_fields_set
)
from ...conversion_helpers.converters import value_deserializer_id, value_serializer_id

from ..application_command import (
    APPLICATION_COMMAND_CONVERSIONS, APPLICATION_ID_CONVERSION, CHANNEL_ID_CONVERSION, GUILD_ID_CONVERSION
)


def test__APPLICATION_COMMAND_CONVERSIONS():
    """
    Tests whether `APPLICATION_COMMAND_CONVERSIONS` contains conversion for every expected key.
    """
    _assert_conversion_group_fields_set(APPLICATION_COMMAND_CONVERSIONS)
    vampytest.assert_eq(
        {conversion.field_key for conversion in APPLICATION_COMMAND_CONVERSIONS.conversions},
        {'application_id', 'channel_id', 'guild_id'},
    )


# ---- application_id ----

def test__APPLICATION_ID_CONVERSION__generic():
    """
    Tests whether ``APPLICATION_ID_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(APPLICATION_ID_CONVERSION)
    vampytest.assert_is(APPLICATION_ID_CONVERSION.value_deserializer, value_deserializer_id)
    vampytest.assert_is(APPLICATION_ID_CONVERSION.value_serializer, value_serializer_id)
    vampytest.assert_is(APPLICATION_ID_CONVERSION.value_validator, validate_application_id)


# ---- channel_id ----

def test__CHANNEL_ID_CONVERSION__generic():
    """
    Tests whether ``CHANNEL_ID_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(CHANNEL_ID_CONVERSION)
    vampytest.assert_is(CHANNEL_ID_CONVERSION.value_deserializer, value_deserializer_id)
    vampytest.assert_is(CHANNEL_ID_CONVERSION.value_serializer, value_serializer_id)
    vampytest.assert_is(CHANNEL_ID_CONVERSION.value_validator, validate_channel_id)


# ---- guild_id ----

def test__GUILD_ID_CONVERSION__generic():
    """
    Tests whether ``GUILD_ID_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(GUILD_ID_CONVERSION)
    vampytest.assert_is(GUILD_ID_CONVERSION.value_deserializer, value_deserializer_id)
    vampytest.assert_is(GUILD_ID_CONVERSION.value_serializer, value_serializer_id)
    vampytest.assert_is(GUILD_ID_CONVERSION.value_validator, validate_guild_id)
