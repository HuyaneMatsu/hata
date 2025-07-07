from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....scheduled_event.scheduled_event_occasion_overwrite.fields import (
    validate_cancelled, validate_end, validate_start, 
)
from ....utils import datetime_to_timestamp

from ...audit_log_entry_change_conversion import AuditLogEntryChangeConversion
from ...audit_log_entry_change_conversion.tests.test__AuditLogEntryChangeConversion import (
    _assert_fields_set as _assert_conversion_fields_set
)
from ...audit_log_entry_change_conversion.tests.test__AuditLogEntryChangeConversionGroup import (
    _assert_fields_set as _assert_conversion_group_fields_set
)

from ..scheduled_event_occasion_overwrite import (
    CANCELLED_CONVERSION, END_CONVERSION, SCHEDULED_EVENT_OCCASION_OVERWRITE_CONVERSIONS, START_CONVERSION
)


def test__SCHEDULED_EVENT_OCCASION_OVERWRITE_CONVERSIONS():
    """
    Tests whether `SCHEDULED_EVENT_OCCASION_OVERWRITE_CONVERSIONS` contains conversion for every expected key.
    """
    _assert_conversion_group_fields_set(SCHEDULED_EVENT_OCCASION_OVERWRITE_CONVERSIONS)
    vampytest.assert_eq(
        {*SCHEDULED_EVENT_OCCASION_OVERWRITE_CONVERSIONS.iter_field_keys()},
        {'is_canceled', 'scheduled_end_time', 'scheduled_start_time',},
    )


# ---- cancelled ----

def test__CANCELLED_CONVERSION__generic():
    """
    Tests whether ``CANCELLED_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(CANCELLED_CONVERSION)
    vampytest.assert_is(CANCELLED_CONVERSION.value_serializer, None)
    vampytest.assert_is(CANCELLED_CONVERSION.value_validator, validate_cancelled)


def _iter_options__cancelled__value_deserializer():
    yield True, True
    yield False, False
    yield None, False


@vampytest._(vampytest.call_from(_iter_options__cancelled__value_deserializer()).returning_last())
def test__CANCELLED_CONVERSION__value_deserializer(input_value):
    """
    Tests whether `CANCELLED_CONVERSION.value_deserializer` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : `bool`
    """
    return CANCELLED_CONVERSION.value_deserializer(input_value)


# ---- end ----

def test__END_CONVERSION__generic():
    """
    Tests whether ``END_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(END_CONVERSION)
    vampytest.assert_is(END_CONVERSION.value_validator, validate_end)


# ---- start ----

def test__START_CONVERSION__generic():
    """
    Tests whether ``START_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(START_CONVERSION)
    vampytest.assert_is(START_CONVERSION.value_validator, validate_start)


# ----


def _iter_options__date_time__value_deserializer():
    date_time = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    yield END_CONVERSION, datetime_to_timestamp(date_time), date_time
    yield END_CONVERSION, None, None
    yield START_CONVERSION, datetime_to_timestamp(date_time), date_time
    yield START_CONVERSION, None, None


@vampytest._(vampytest.call_from(_iter_options__date_time__value_deserializer()).returning_last())
def test__DATE_TIME_CONVERSION__value_deserializer(conversion, input_value):
    """
    Tests whether `START_CONVERSION.value_deserializer` and `END_CONVERSION.value_deserializer` works as intended.
    
    Parameters
    ----------
    conversion : ``AuditLogEntryChangeConversion``
        Conversion to test.
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : `None | DateTime`
    """
    return conversion.value_deserializer(input_value)


def _iter_options__date_time__value_serializer():
    date_time = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    yield END_CONVERSION, date_time, datetime_to_timestamp(date_time)
    yield END_CONVERSION, None, None
    yield START_CONVERSION, date_time, datetime_to_timestamp(date_time)
    yield START_CONVERSION, None, None


@vampytest._(vampytest.call_from(_iter_options__date_time__value_serializer()).returning_last())
def test__DATE_TIME_CONVERSION__value_serializer(conversion, input_value):
    """
    Tests whether `START_CONVERSION.value_serializer` and `END_CONVERSION.value_serializer` works as intended.
    
    Parameters
    ----------
    conversion : ``AuditLogEntryChangeConversion``
        Conversion to test.
    input_value : `None | DateTime`
        Processed value.
    
    Returns
    -------
    output : `None | str`
    """
    return conversion.value_serializer(input_value)
