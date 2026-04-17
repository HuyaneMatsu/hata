import vampytest

from ....onboarding import OnboardingPromptOption, OnboardingPromptType
from ....onboarding.onboarding_prompt.fields import (
    validate_in_onboarding, validate_name, validate_options, validate_required, validate_single_select, validate_type
)

from ...audit_log_entry_change_conversion.tests.test__AuditLogEntryChangeConversion import (
    _assert_fields_set as _assert_conversion_fields_set
)
from ...audit_log_entry_change_conversion.tests.test__AuditLogEntryChangeConversionGroup import (
    _assert_fields_set as _assert_conversion_group_fields_set
)
from ...conversion_helpers.converters import value_deserializer_name, value_serializer_name

from ..onboarding_prompt import (
    IN_ONBOARDING_CONVERSION, NAME_CONVERSION, ONBOARDING_PROMPT_CONVERSIONS, OPTIONS_CONVERSION, REQUIRED_CONVERSION,
    SINGLE_SELECT_CONVERSION, TYPE_CONVERSION
)


def test__ONBOARDING_PROMPT_CONVERSIONS():
    """
    Tests whether `ONBOARDING_PROMPT_CONVERSIONS` contains conversion for every expected key.
    """
    _assert_conversion_group_fields_set(ONBOARDING_PROMPT_CONVERSIONS)
    vampytest.assert_eq(
        {*ONBOARDING_PROMPT_CONVERSIONS.iter_field_keys()},
        {'in_onboarding', 'title', 'options', 'required', 'single_select', 'type'},
    )


# ---- in_onboarding ----

def test__IN_ONBOARDING_CONVERSION__generic():
    """
    Tests whether ``IN_ONBOARDING_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(IN_ONBOARDING_CONVERSION)
    vampytest.assert_is(IN_ONBOARDING_CONVERSION.value_serializer, None)
    vampytest.assert_is(IN_ONBOARDING_CONVERSION.value_validator, validate_in_onboarding)


def _iter_options__in_onboarding__value_deserializer():
    yield True, True
    yield False, False
    yield None, False


@vampytest._(vampytest.call_from(_iter_options__in_onboarding__value_deserializer()).returning_last())
def test__IN_ONBOARDING_CONVERSION__value_deserializer(input_value):
    """
    Tests whether `IN_ONBOARDING_CONVERSION.value_deserializer` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : `bool`
    """
    return IN_ONBOARDING_CONVERSION.value_deserializer(input_value)


# ---- name ----

def test__NAME_CONVERSION__generic():
    """
    Tests whether ``NAME_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(NAME_CONVERSION)
    vampytest.assert_is(NAME_CONVERSION.value_deserializer, value_deserializer_name)
    vampytest.assert_is(NAME_CONVERSION.value_serializer, value_serializer_name)
    vampytest.assert_is(NAME_CONVERSION.value_validator, validate_name)


# ---- options ----

def test__OPTIONS_CONVERSION__generic():
    """
    Tests whether ``OPTIONS_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(OPTIONS_CONVERSION)
    vampytest.assert_is(OPTIONS_CONVERSION.value_validator, validate_options)
    

def _iter_options__options__value_deserializer():
    option_0 = OnboardingPromptOption.precreate(202310250000)
    option_1 = OnboardingPromptOption.precreate(202310250001)
    
    yield None, None
    yield [], None
    yield (
        [
            option_0.to_data(defaults = True, include_internals = True),
            option_1.to_data(defaults = True, include_internals = True),
        ],
        (option_0, option_1),
    )


@vampytest._(vampytest.call_from(_iter_options__options__value_deserializer()).returning_last())
def test__OPTIONS_CONVERSION__value_deserializer(input_value):
    """
    Tests whether `OPTIONS_CONVERSION.value_deserializer` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : `None | tuple<OnboardingPromptOption>`
    """
    return OPTIONS_CONVERSION.value_deserializer(input_value)


def _iter_options__options__value_serializer():
    option_0 = OnboardingPromptOption.precreate(202310250002)
    option_1 = OnboardingPromptOption.precreate(202310250003)
    
    yield None, []
    yield (
        (option_0, option_1),
        [
            option_0.to_data(defaults = True, include_internals = True),
            option_1.to_data(defaults = True, include_internals = True),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options__options__value_serializer()).returning_last())
def test__OPTIONS_CONVERSION__value_serializer(input_value):
    """
    Tests whether `OPTIONS_CONVERSION.value_serializer` works as intended.
    
    Parameters
    ----------
    input_value : `None | tuple<OnboardingPromptOption>`
        Processed value.
    
    Returns
    -------
    output : `list<dict<str, object>>`
    """
    return OPTIONS_CONVERSION.value_serializer(input_value)


# ---- required ----

def test__REQUIRED_CONVERSION__generic():
    """
    Tests whether ``REQUIRED_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(REQUIRED_CONVERSION)
    vampytest.assert_is(REQUIRED_CONVERSION.value_serializer, None)
    vampytest.assert_is(REQUIRED_CONVERSION.value_validator, validate_required)


def _iter_options__required__value_deserializer():
    yield True, True
    yield False, False
    yield None, False


@vampytest._(vampytest.call_from(_iter_options__required__value_deserializer()).returning_last())
def test__REQUIRED_CONVERSION__value_deserializer(input_value):
    """
    Tests whether `REQUIRED_CONVERSION.value_deserializer` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : `bool`
    """
    return REQUIRED_CONVERSION.value_deserializer(input_value)


# ---- single_select ----

def test__SINGLE_SELECT_CONVERSION__generic():
    """
    Tests whether ``SINGLE_SELECT_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(SINGLE_SELECT_CONVERSION)
    vampytest.assert_is(SINGLE_SELECT_CONVERSION.value_serializer, None)
    vampytest.assert_is(SINGLE_SELECT_CONVERSION.value_validator, validate_single_select)


def _iter_options__single_select__value_deserializer():
    yield True, True
    yield False, False
    yield None, False


@vampytest._(vampytest.call_from(_iter_options__single_select__value_deserializer()).returning_last())
def test__SINGLE_SELECT_CONVERSION__value_deserializer(input_value):
    """
    Tests whether `SINGLE_SELECT_CONVERSION.value_deserializer` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : `bool`
    """
    return SINGLE_SELECT_CONVERSION.value_deserializer(input_value)

# ---- type ----

def test__TYPE_CONVERSION__generic():
    """
    Tests whether ``TYPE_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(TYPE_CONVERSION)
    vampytest.assert_is(TYPE_CONVERSION.value_validator, validate_type)


def _iter_options__type__value_deserializer():
    yield None, OnboardingPromptType.multiple_choice
    yield OnboardingPromptType.dropdown.value, OnboardingPromptType.dropdown


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
    output : ``OnboardingPromptType``
    """
    return TYPE_CONVERSION.value_deserializer(input_value)


def _iter_options__type__value_serializer():
    yield OnboardingPromptType.multiple_choice, OnboardingPromptType.multiple_choice.value
    yield OnboardingPromptType.dropdown, OnboardingPromptType.dropdown.value


@vampytest._(vampytest.call_from(_iter_options__type__value_serializer()).returning_last())
def test__TYPE_CONVERSION__value_serializer(input_value):
    """
    Tests whether `TYPE_CONVERSION.value_serializer` works as intended.
    
    Parameters
    ----------
    input_value : ``OnboardingPromptType``
        Processed value.
    
    Returns
    -------
    output : `int`
    """
    return TYPE_CONVERSION.value_serializer(input_value)
