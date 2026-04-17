import vampytest

from ....integration import IntegrationExpireBehavior, IntegrationType
from ....integration.integration.fields import validate_name, validate_type
from ....integration.integration_metadata.constants import EXPIRE_GRACE_PERIOD_DEFAULT
from ....integration.integration_metadata.fields import (
    validate_emojis_enabled, validate_expire_behavior, validate_expire_grace_period
)

from ...audit_log_entry_change_conversion.tests.test__AuditLogEntryChangeConversion import (
    _assert_fields_set as _assert_conversion_fields_set
)
from ...audit_log_entry_change_conversion.tests.test__AuditLogEntryChangeConversionGroup import (
    _assert_fields_set as _assert_conversion_group_fields_set
)
from ...conversion_helpers.converters import value_deserializer_name, value_serializer_name

from ..integration import (
    EMOJIS_ENABLED_CONVERSION, EXPIRE_BEHAVIOR_CONVERSION, EXPIRE_GRACE_PERIOD_CONVERSION, INTEGRATION_CONVERSIONS,
    NAME_CONVERSION, TYPE_CONVERSION
)


def test__INTEGRATION_CONVERSIONS():
    """
    Tests whether `INTEGRATION_CONVERSIONS` contains conversion for every expected key.
    """
    _assert_conversion_group_fields_set(INTEGRATION_CONVERSIONS)
    vampytest.assert_eq(
        {*INTEGRATION_CONVERSIONS.iter_field_keys()},
        {'enable_emoticons', 'expire_behavior', 'expire_grace_period', 'name', 'type'},
    )


# ---- emojis_enabled ----

def test__EMOJIS_ENABLED_CONVERSION__generic():
    """
    Tests whether ``EMOJIS_ENABLED_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(EMOJIS_ENABLED_CONVERSION)
    vampytest.assert_is(EMOJIS_ENABLED_CONVERSION.value_serializer, None)
    vampytest.assert_is(EMOJIS_ENABLED_CONVERSION.value_validator, validate_emojis_enabled)


def _iter_options__emojis_enabled__value_deserializer():
    yield True, True
    yield False, False
    yield None, True


@vampytest._(vampytest.call_from(_iter_options__emojis_enabled__value_deserializer()).returning_last())
def test__EMOJIS_ENABLED_CONVERSION__value_deserializer(input_value):
    """
    Tests whether `EMOJIS_ENABLED_CONVERSION.value_deserializer` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : `bool`
    """
    return EMOJIS_ENABLED_CONVERSION.value_deserializer(input_value)


# ---- expire_behavior ----

def test__EXPIRE_BEHAVIOR_CONVERSION__generic():
    """
    Tests whether ``EXPIRE_BEHAVIOR_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(EXPIRE_BEHAVIOR_CONVERSION)
    vampytest.assert_is(EXPIRE_BEHAVIOR_CONVERSION.value_validator, validate_expire_behavior)


def _iter_options__expire_behavior__value_deserializer():
    yield None, IntegrationExpireBehavior.remove_role
    yield IntegrationExpireBehavior.kick.value, IntegrationExpireBehavior.kick


@vampytest._(vampytest.call_from(_iter_options__expire_behavior__value_deserializer()).returning_last())
def test__EXPIRE_BEHAVIOR_CONVERSION__value_deserializer(input_value):
    """
    Tests whether `EXPIRE_BEHAVIOR_CONVERSION.value_deserializer` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : ``IntegrationExpireBehavior``
    """
    return EXPIRE_BEHAVIOR_CONVERSION.value_deserializer(input_value)


def _iter_options__expire_behavior__value_serializer():
    yield IntegrationExpireBehavior.remove_role, IntegrationExpireBehavior.remove_role.value
    yield IntegrationExpireBehavior.kick, IntegrationExpireBehavior.kick.value


@vampytest._(vampytest.call_from(_iter_options__expire_behavior__value_serializer()).returning_last())
def test__EXPIRE_BEHAVIOR_CONVERSION__value_serializer(input_value):
    """
    Tests whether `EXPIRE_BEHAVIOR_CONVERSION.value_serializer` works as intended.
    
    Parameters
    ----------
    input_value : ``IntegrationExpireBehavior``
        Processed value.
    
    Returns
    -------
    output : `int`
    """
    return EXPIRE_BEHAVIOR_CONVERSION.value_serializer(input_value)


# ---- expire_grace_period ----

def test__EXPIRE_GRACE_PERIOD_CONVERSION__generic():
    """
    Tests whether ``EXPIRE_GRACE_PERIOD_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(EXPIRE_GRACE_PERIOD_CONVERSION)
    vampytest.assert_is(EXPIRE_GRACE_PERIOD_CONVERSION.value_serializer, None)
    vampytest.assert_is(EXPIRE_GRACE_PERIOD_CONVERSION.value_validator, validate_expire_grace_period)


def _iter_options__expire_grace_period__value_deserializer():
    yield 60, 60
    yield 0, 0
    yield None, EXPIRE_GRACE_PERIOD_DEFAULT


@vampytest._(vampytest.call_from(_iter_options__expire_grace_period__value_deserializer()).returning_last())
def test__EXPIRE_GRACE_PERIOD_CONVERSION__value_deserializer(input_value):
    """
    Tests whether `EXPIRE_GRACE_PERIOD_CONVERSION.value_deserializer` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : `int`
    """
    return EXPIRE_GRACE_PERIOD_CONVERSION.value_deserializer(input_value)


# ---- name ----

def test__NAME_CONVERSION__generic():
    """
    Tests whether ``NAME_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(NAME_CONVERSION)
    vampytest.assert_is(NAME_CONVERSION.value_deserializer, value_deserializer_name)
    vampytest.assert_is(NAME_CONVERSION.value_serializer, value_serializer_name)
    vampytest.assert_is(NAME_CONVERSION.value_validator, validate_name)


# ---- type ----

def test__TYPE_CONVERSION__generic():
    """
    Tests whether ``TYPE_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(TYPE_CONVERSION)
    vampytest.assert_is(TYPE_CONVERSION.value_validator, validate_type)


def _iter_options__type__value_deserializer():
    yield None, IntegrationType.none
    yield IntegrationType.discord.value, IntegrationType.discord


@vampytest._(vampytest.call_from(_iter_options__type__value_deserializer()).returning_last())
def test__TYPE_CONVERSION__value_deserializer(input_value):
    """
    Tests whether `TYPE_CONVERSION.value_deserializer` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : ``IntegrationType``
    """
    return TYPE_CONVERSION.value_deserializer(input_value)


def _iter_options__type__value_serializer():
    yield IntegrationType.none, IntegrationType.none.value
    yield IntegrationType.discord, IntegrationType.discord.value


@vampytest._(vampytest.call_from(_iter_options__type__value_serializer()).returning_last())
def test__TYPE_CONVERSION__value_serializer(input_value):
    """
    Tests whether `TYPE_CONVERSION.value_serializer` works as intended.
    
    Parameters
    ----------
    input_value : ``IntegrationType``
        Processed value.
    
    Returns
    -------
    output : `str`
    """
    return TYPE_CONVERSION.value_serializer(input_value)
