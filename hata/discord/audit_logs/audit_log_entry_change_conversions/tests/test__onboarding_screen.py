import vampytest

from ....onboarding import OnboardingMode, OnboardingPrompt
from ....onboarding.onboarding_screen.fields import (
    validate_default_channel_ids, validate_enabled, validate_mode, validate_prompts
)

from ...audit_log_entry_change_conversion.change_deserializers import change_deserializer_deprecation
from ...audit_log_entry_change_conversion.tests.test__AuditLogEntryChangeConversion import (
    _assert_fields_set as _assert_conversion_fields_set
)
from ...audit_log_entry_change_conversion.tests.test__AuditLogEntryChangeConversionGroup import (
    _assert_fields_set as _assert_conversion_group_fields_set
)
from ...conversion_helpers.converters import value_deserializer_ids, value_serializer_ids

from ..onboarding_screen import (
    BELOW_REQUIREMENTS_CONVERSION_IGNORED, DEFAULT_CHANNEL_IDS_CONVERSION, ENABLED_CONVERSION, MODE_CONVERSION,
    ONBOARDING_SCREEN_CONVERSIONS, PROMPTS_CONVERSION
)


def test__ONBOARDING_SCREEN_CONVERSIONS():
    """
    Tests whether `ONBOARDING_SCREEN_CONVERSIONS` contains conversion for every expected key.
    """
    _assert_conversion_group_fields_set(ONBOARDING_SCREEN_CONVERSIONS)
    vampytest.assert_eq(
        {*ONBOARDING_SCREEN_CONVERSIONS.iter_field_keys()},
        {'default_channel_ids', 'enabled', 'prompts', 'below_requirements', 'mode'},
    )


# ---- default_channel_ids ----

def test__DEFAULT_CHANNEL_IDS_CONVERSION__generic():
    """
    Tests whether ``DEFAULT_CHANNEL_IDS_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(DEFAULT_CHANNEL_IDS_CONVERSION)
    vampytest.assert_is(DEFAULT_CHANNEL_IDS_CONVERSION.value_deserializer, value_deserializer_ids)
    vampytest.assert_is(DEFAULT_CHANNEL_IDS_CONVERSION.value_serializer, value_serializer_ids)
    vampytest.assert_is(DEFAULT_CHANNEL_IDS_CONVERSION.value_validator, validate_default_channel_ids)


# ---- enabled ----

def test__ENABLED_CONVERSION__generic():
    """
    Tests whether ``ENABLED_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(ENABLED_CONVERSION)
    vampytest.assert_is(ENABLED_CONVERSION.value_serializer, None)
    vampytest.assert_is(ENABLED_CONVERSION.value_validator, validate_enabled)


def _iter_options__enabled__value_deserializer():
    yield True, True
    yield False, False
    yield None, True


@vampytest._(vampytest.call_from(_iter_options__enabled__value_deserializer()).returning_last())
def test__ENABLED_CONVERSION__value_deserializer(input_value):
    """
    Tests whether `ENABLED_CONVERSION.value_deserializer` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : `bool`
    """
    return ENABLED_CONVERSION.value_deserializer(input_value)


# ---- mode ----

def test__MODE_CONVERSION__generic():
    """
    Tests whether ``MODE_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(MODE_CONVERSION)
    vampytest.assert_is(MODE_CONVERSION.value_validator, validate_mode)


def _iter_options__mode__value_deserializer():
    yield None, OnboardingMode.default
    yield OnboardingMode.advanced.value, OnboardingMode.advanced


@vampytest._(vampytest.call_from(_iter_options__mode__value_deserializer()).returning_last())
def test__MODE_CONVERSION__value_deserializer(input_value):
    """
    Tests whether `MODE_CONVERSION.value_deserializer` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : ``OnboardingMode``
    """
    return MODE_CONVERSION.value_deserializer(input_value)


def _iter_options__mode__value_serializer():
    yield OnboardingMode.default, OnboardingMode.default.value
    yield OnboardingMode.advanced, OnboardingMode.advanced.value


@vampytest._(vampytest.call_from(_iter_options__mode__value_serializer()).returning_last())
def test__MODE_CONVERSION__value_serializer(input_value):
    """
    Tests whether `MODE_CONVERSION.value_serializer` works as intended.
    
    Parameters
    ----------
    input_value : ``OnboardingMode``
        Processed value.
    
    Returns
    -------
    output : `str`
    """
    return MODE_CONVERSION.value_serializer(input_value)


# ---- prompts ----

def test__PROMPTS_CONVERSION__generic():
    """
    Tests whether ``PROMPTS_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(PROMPTS_CONVERSION)
    vampytest.assert_is(PROMPTS_CONVERSION.value_validator, validate_prompts)
    

def _iter_prompts__prompts__value_deserializer():
    prompt_0 = OnboardingPrompt.precreate(202310250004)
    prompt_1 = OnboardingPrompt.precreate(202310250005)
    
    yield None, None
    yield [], None
    yield (
        [
            prompt_0.to_data(defaults = True, include_internals = True),
            prompt_1.to_data(defaults = True, include_internals = True),
        ],
        (prompt_0, prompt_1),
    )


@vampytest._(vampytest.call_from(_iter_prompts__prompts__value_deserializer()).returning_last())
def test__PROMPTS_CONVERSION__value_deserializer(input_value):
    """
    Tests whether `PROMPTS_CONVERSION.value_deserializer` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : `None | tuple<OnboardingPrompt>`
    """
    return PROMPTS_CONVERSION.value_deserializer(input_value)


def _iter_prompts__prompts__value_serializer():
    prompt_0 = OnboardingPrompt.precreate(202310250006)
    prompt_1 = OnboardingPrompt.precreate(202310250007)
    
    yield None, []
    yield (
        (prompt_0, prompt_1),
        [
            prompt_0.to_data(defaults = True, include_internals = True),
            prompt_1.to_data(defaults = True, include_internals = True),
        ],
    )


@vampytest._(vampytest.call_from(_iter_prompts__prompts__value_serializer()).returning_last())
def test__PROMPTS_CONVERSION__value_serializer(input_value):
    """
    Tests whether `PROMPTS_CONVERSION.value_serializer` works as intended.
    
    Parameters
    ----------
    input_value : `None | tuple<OnboardingPrompt>`
        Processed value.
    
    Returns
    -------
    output : `list<dict<str, object>>`
    """
    return PROMPTS_CONVERSION.value_serializer(input_value)


# ---- ignored ----

def _iter_options__ignored():
    yield BELOW_REQUIREMENTS_CONVERSION_IGNORED


@vampytest.call_from(_iter_options__ignored())
def test_ignored(conversion):
    """
    Tests whether the ignored conversions are set up as intended.
    
    Parameters
    ----------
    conversion : ``AuditLogEntryChangeConversion``
        The conversion to test.
    """
    _assert_conversion_fields_set(conversion)
    vampytest.assert_is(conversion.change_deserializer, change_deserializer_deprecation)
    vampytest.assert_eq(conversion.field_name, '')

