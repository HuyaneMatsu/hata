from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....scheduled_event.scheduled_event_occasion_overwrite.fields import validate_timestamp
from ....utils import DISCORD_EPOCH_START, datetime_to_id

from ...audit_log_entry_detail_conversion.tests.test__AuditLogEntryDetailConversion import (
    _assert_fields_set as _assert_conversion_fields_set
)
from ...audit_log_entry_detail_conversion.tests.test__AuditLogEntryDetailConversionGroup import (
    _assert_fields_set as _assert_conversion_group_fields_set
)
from ..scheduled_event_occasion_overwrite import TIMESTAMP_CONVERSION, SCHEDULED_EVENT_OCCASION_OVERWRITE_CONVERSIONS


def test__SCHEDULED_EVENT_OCCASION_OVERWRITE_CONVERSIONS():
    """
    Tests whether `SCHEDULED_EVENT_OCCASION_OVERWRITE_CONVERSIONS` contains conversion for every expected key.
    """
    _assert_conversion_group_fields_set(SCHEDULED_EVENT_OCCASION_OVERWRITE_CONVERSIONS)
    vampytest.assert_eq(
        {conversion.field_key for conversion in SCHEDULED_EVENT_OCCASION_OVERWRITE_CONVERSIONS.conversions},
        {'event_exception_id',}
    )


# ---- timestamp ----

def test__TIMESTAMP_CONVERSION__generic():
    """
    Tests whether ``TIMESTAMP_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(TIMESTAMP_CONVERSION)
    vampytest.assert_is(TIMESTAMP_CONVERSION.value_validator, validate_timestamp)


def _iter_options__timestamp__value_deserializer():
    timestamp = DateTime(2016, 5, 14, 13, 0, 0, tzinfo = TimeZone.utc)
    
    yield None, DISCORD_EPOCH_START
    yield str(datetime_to_id(timestamp)), timestamp


@vampytest._(vampytest.call_from(_iter_options__timestamp__value_deserializer()).returning_last())
def test__TIMESTAMP_CONVERSION__value_deserializer(input_value):
    """
    Tests whether `TIMESTAMP_CONVERSION.value_deserializer` works as intended.
    
    Parameters
    ----------
    input_value : `None | int`
        Raw value.
    
    Returns
    -------
    output : `DateTime`
    """
    output = TIMESTAMP_CONVERSION.value_deserializer(input_value)
    vampytest.assert_instance(output, DateTime)
    return output


def _iter_options__timestamp__value_serializer():
    timestamp = DateTime(2016, 5, 14, 13, 0, 0, tzinfo = TimeZone.utc)
    
    yield timestamp, str(datetime_to_id(timestamp))


@vampytest._(vampytest.call_from(_iter_options__timestamp__value_serializer()).returning_last())
def test__TIMESTAMP_CONVERSION__value_serializer(input_value):
    """
    Tests whether `TIMESTAMP_CONVERSION.value_serializer` works as intended.
    
    Parameters
    ----------
    input_value : `DateTime`
        Raw value.
    
    Returns
    -------
    output : `str`
    """
    output = TIMESTAMP_CONVERSION.value_serializer(input_value)
    vampytest.assert_instance(output, str)
    return output
