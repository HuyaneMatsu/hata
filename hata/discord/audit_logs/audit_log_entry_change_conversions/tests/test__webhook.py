import vampytest

from ....bases import Icon
from ....user.user.fields import validate_name
from ....user.user.user_base import USER_AVATAR
from ....webhook import WebhookType
from ....webhook.webhook.fields import validate_application_id, validate_channel_id, validate_type

from ...audit_log_entry_change_conversion.tests.test__AuditLogEntryChangeConversion import (
    _assert_fields_set as _assert_conversion_fields_set
)
from ...audit_log_entry_change_conversion.tests.test__AuditLogEntryChangeConversionGroup import (
    _assert_fields_set as _assert_conversion_group_fields_set
)
from ...conversion_helpers.converters import get_converter_id, get_converter_name, put_converter_id, put_converter_name

from ..webhook import (
    APPLICATION_ID_CONVERSION, AVATAR_CONVERSION, CHANNEL_ID_CONVERSION, NAME_CONVERSION, TYPE_CONVERSION,
    WEBHOOK_CONVERSIONS
)


def test__WEBHOOK_CONVERSIONS():
    """
    Tests whether `WEBHOOK_CONVERSIONS` contains conversion for every expected key.
    """
    _assert_conversion_group_fields_set(WEBHOOK_CONVERSIONS)
    vampytest.assert_eq(
        {*WEBHOOK_CONVERSIONS.get_converters.keys()},
        {'application_id', 'avatar_hash', 'channel_id', 'name', 'type'},
    )


# ---- application_id ----

def test__APPLICATION_ID_CONVERSION__generic():
    """
    Tests whether ``APPLICATION_ID_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(APPLICATION_ID_CONVERSION)
    vampytest.assert_is(APPLICATION_ID_CONVERSION.get_converter, get_converter_id)
    vampytest.assert_is(APPLICATION_ID_CONVERSION.put_converter, put_converter_id)
    vampytest.assert_is(APPLICATION_ID_CONVERSION.validator, validate_application_id)


# ---- avatar ----

def test__AVATAR_CONVERSION__generic():
    """
    Tests whether ``AVATAR_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(AVATAR_CONVERSION)
    vampytest.assert_eq(AVATAR_CONVERSION.get_converter, Icon.from_base_16_hash)
    vampytest.assert_eq(AVATAR_CONVERSION.put_converter, Icon.as_base_16_hash.fget)
    vampytest.assert_eq(AVATAR_CONVERSION.validator, USER_AVATAR.validate_icon)


# ---- channel_id ----

def test__CHANNEL_ID_CONVERSION__generic():
    """
    Tests whether ``CHANNEL_ID_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(CHANNEL_ID_CONVERSION)
    vampytest.assert_is(CHANNEL_ID_CONVERSION.get_converter, get_converter_id)
    vampytest.assert_is(CHANNEL_ID_CONVERSION.put_converter, put_converter_id)
    vampytest.assert_is(CHANNEL_ID_CONVERSION.validator, validate_channel_id)


# ---- name ----

def test__NAME_CONVERSION__generic():
    """
    Tests whether ``NAME_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(NAME_CONVERSION)
    vampytest.assert_is(NAME_CONVERSION.get_converter, get_converter_name)
    vampytest.assert_is(NAME_CONVERSION.put_converter, put_converter_name)
    vampytest.assert_is(NAME_CONVERSION.validator, validate_name)



# ---- type ----

def test__TYPE_CONVERSION__generic():
    """
    Tests whether ``TYPE_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(TYPE_CONVERSION)
    # vampytest.assert_is(TYPE_CONVERSION.get_converter, )
    # vampytest.assert_is(TYPE_CONVERSION.put_converter, )
    vampytest.assert_is(TYPE_CONVERSION.validator, validate_type)


def _iter_options__type__get_converter():
    yield None, WebhookType.none
    yield WebhookType.server.value, WebhookType.server


@vampytest._(vampytest.call_from(_iter_options__type__get_converter()).returning_last())
def test__TYPE_CONVERSION__get_converter(input_value):
    """
    Tests whether `TYPE_CONVERSION.get_converter` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : ``WebhookType``
    """
    return TYPE_CONVERSION.get_converter(input_value)


def _iter_options__type__put_converter():
    yield WebhookType.none, WebhookType.none.value
    yield WebhookType.server, WebhookType.server.value


@vampytest._(vampytest.call_from(_iter_options__type__put_converter()).returning_last())
def test__TYPE_CONVERSION__put_converter(input_value):
    """
    Tests whether `TYPE_CONVERSION.put_converter` works as intended.
    
    Parameters
    ----------
    input_value : ``WebhookType``
        Processed value.
    
    Returns
    -------
    output : `int`
    """
    return TYPE_CONVERSION.put_converter(input_value)
