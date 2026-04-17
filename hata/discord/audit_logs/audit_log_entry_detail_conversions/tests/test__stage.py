import vampytest

from ....stage.stage.fields import validate_channel_id

from ...audit_log_entry_detail_conversion.tests.test__AuditLogEntryDetailConversion import (
    _assert_fields_set as _assert_conversion_fields_set
)
from ...audit_log_entry_detail_conversion.tests.test__AuditLogEntryDetailConversionGroup import (
    _assert_fields_set as _assert_conversion_group_fields_set
)
from ...conversion_helpers.converters import value_deserializer_id, value_serializer_id

from ..stage import CHANNEL_ID_CONVERSION, STAGE_CONVERSIONS


def test__STAGE_CONVERSIONS():
    """
    Tests whether `STAGE_CONVERSIONS` contains conversion for every expected key.
    """
    _assert_conversion_group_fields_set(STAGE_CONVERSIONS)
    vampytest.assert_eq(
        {conversion.field_key for conversion in STAGE_CONVERSIONS.conversions},
        {'channel_id',}
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
