import vampytest

from ....channel.channel.fields import validate_id
from ....channel.channel_metadata.fields import validate_status

from ...audit_log_entry_detail_conversion.tests.test__AuditLogEntryDetailConversion import (
    _assert_fields_set as _assert_conversion_fields_set
)
from ...audit_log_entry_detail_conversion.tests.test__AuditLogEntryDetailConversionGroup import (
    _assert_fields_set as _assert_conversion_group_fields_set
)
from ...conversion_helpers.converters import (
    value_deserializer_description, value_deserializer_id, value_serializer_description, value_serializer_id
)

from ..channel import CHANNEL_CONVERSIONS, ID_CONVERSION, STATUS_CONVERSION


def test__CHANNEL_CONVERSIONS():
    """
    Tests whether `CHANNEL_CONVERSIONS` contains conversion for every expected key.
    """
    _assert_conversion_group_fields_set(CHANNEL_CONVERSIONS)
    vampytest.assert_eq(
        {conversion.field_key for conversion in CHANNEL_CONVERSIONS.conversions},
        {'status', 'channel_id'}
    )


# ---- status ----

def test__STATUS_CONVERSION__generic():
    """
    Tests whether ``STATUS_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(STATUS_CONVERSION)
    vampytest.assert_is(STATUS_CONVERSION.value_deserializer, value_deserializer_description)
    vampytest.assert_is(STATUS_CONVERSION.value_serializer, value_serializer_description)
    vampytest.assert_is(STATUS_CONVERSION.value_validator, validate_status)


# ---- id ----

def test__ID_CONVERSION__generic():
    """
    Tests whether ``ID_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(ID_CONVERSION)
    vampytest.assert_is(ID_CONVERSION.value_deserializer, value_deserializer_id)
    vampytest.assert_is(ID_CONVERSION.value_serializer, value_serializer_id)
    vampytest.assert_is(ID_CONVERSION.value_validator, validate_id)
