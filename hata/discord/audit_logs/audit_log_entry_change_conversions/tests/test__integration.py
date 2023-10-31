import vampytest

from ....integration import IntegrationExpireBehavior
from ....integration.integration_metadata.constants import EXPIRE_GRACE_PERIOD_DEFAULT
from ....integration.integration_metadata.fields import (
    validate_emojis_enabled, validate_expire_behavior, validate_expire_grace_period
)

from ..integration import (
    EMOJIS_ENABLED_CONVERSION, EXPIRE_BEHAVIOR_CONVERSION, EXPIRE_GRACE_PERIOD_CONVERSION, INTEGRATION_CONVERSIONS
)

def test__INTEGRATION_CONVERSIONS():
    """
    Tests whether `INTEGRATION_CONVERSIONS` contains conversion for every expected key.
    """
    vampytest.assert_eq(
        {*INTEGRATION_CONVERSIONS.get_converters.keys()},
        {'enable_emoticons', 'expire_behavior', 'expire_grace_period'},
    )


# ---- emojis_enabled ----

def test__EMOJIS_ENABLED_CONVERSION__generic():
    """
    Tests whether ``EMOJIS_ENABLED_CONVERSION`` works as intended.
    """
    # vampytest.assert_is(EMOJIS_ENABLED_CONVERSION.get_converter, )
    # vampytest.assert_is(EMOJIS_ENABLED_CONVERSION.put_converter, )
    vampytest.assert_is(EMOJIS_ENABLED_CONVERSION.validator, validate_emojis_enabled)


def _iter_options__emojis_enabled__get_converter():
    yield True, True
    yield False, False
    yield None, True


@vampytest._(vampytest.call_from(_iter_options__emojis_enabled__get_converter()).returning_last())
def test__EMOJIS_ENABLED_CONVERSION__get_converter(input_value):
    """
    Tests whether `EMOJIS_ENABLED_CONVERSION.get_converter` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : `bool`
    """
    return EMOJIS_ENABLED_CONVERSION.get_converter(input_value)


def _iter_options__emojis_enabled__put_converter():
    yield True, True
    yield False, False


@vampytest._(vampytest.call_from(_iter_options__emojis_enabled__put_converter()).returning_last())
def test__EMOJIS_ENABLED_CONVERSION__put_converter(input_value):
    """
    Tests whether `EMOJIS_ENABLED_CONVERSION.put_converter` works as intended.
    
    Parameters
    ----------
    input_value : `bool`
        Processed value.
    
    Returns
    -------
    output : `bool`
    """
    return EMOJIS_ENABLED_CONVERSION.put_converter(input_value)


# ---- expire_behavior ----

def test__EXPIRE_BEHAVIOR_CONVERSION__generic():
    """
    Tests whether ``EXPIRE_BEHAVIOR_CONVERSION`` works as intended.
    """
    # vampytest.assert_is(EXPIRE_BEHAVIOR_CONVERSION.get_converter, )
    # vampytest.assert_is(EXPIRE_BEHAVIOR_CONVERSION.put_converter, )
    vampytest.assert_is(EXPIRE_BEHAVIOR_CONVERSION.validator, validate_expire_behavior)


def _iter_options__expire_behavior__get_converter():
    yield None, IntegrationExpireBehavior.remove_role
    yield IntegrationExpireBehavior.kick.value, IntegrationExpireBehavior.kick


@vampytest._(vampytest.call_from(_iter_options__expire_behavior__get_converter()).returning_last())
def test__EXPIRE_BEHAVIOR_CONVERSION__get_converter(input_value):
    """
    Tests whether `EXPIRE_BEHAVIOR_CONVERSION.get_converter` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : ``IntegrationExpireBehavior``
    """
    return EXPIRE_BEHAVIOR_CONVERSION.get_converter(input_value)


def _iter_options__expire_behavior__put_converter():
    yield IntegrationExpireBehavior.remove_role, IntegrationExpireBehavior.remove_role.value
    yield IntegrationExpireBehavior.kick, IntegrationExpireBehavior.kick.value


@vampytest._(vampytest.call_from(_iter_options__expire_behavior__put_converter()).returning_last())
def test__EXPIRE_BEHAVIOR_CONVERSION__put_converter(input_value):
    """
    Tests whether `EXPIRE_BEHAVIOR_CONVERSION.put_converter` works as intended.
    
    Parameters
    ----------
    input_value : ``IntegrationExpireBehavior``
        Processed value.
    
    Returns
    -------
    output : `int`
    """
    return EXPIRE_BEHAVIOR_CONVERSION.put_converter(input_value)


# ---- expire_grace_period ----

def test__EXPIRE_GRACE_PERIOD_CONVERSION__generic():
    """
    Tests whether ``EXPIRE_GRACE_PERIOD_CONVERSION`` works as intended.
    """
    # vampytest.assert_is(EXPIRE_GRACE_PERIOD_CONVERSION.get_converter, )
    # vampytest.assert_is(EXPIRE_GRACE_PERIOD_CONVERSION.put_converter, )
    vampytest.assert_is(EXPIRE_GRACE_PERIOD_CONVERSION.validator, validate_expire_grace_period)


def _iter_options__expire_grace_period__get_converter():
    yield 60, 60
    yield 0, 0
    yield None, EXPIRE_GRACE_PERIOD_DEFAULT


@vampytest._(vampytest.call_from(_iter_options__expire_grace_period__get_converter()).returning_last())
def test__EXPIRE_GRACE_PERIOD_CONVERSION__get_converter(input_value):
    """
    Tests whether `EXPIRE_GRACE_PERIOD_CONVERSION.get_converter` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : `int`
    """
    return EXPIRE_GRACE_PERIOD_CONVERSION.get_converter(input_value)


def _iter_options__expire_grace_period__put_converter():
    yield 60, 60
    yield EXPIRE_GRACE_PERIOD_DEFAULT, EXPIRE_GRACE_PERIOD_DEFAULT


@vampytest._(vampytest.call_from(_iter_options__expire_grace_period__put_converter()).returning_last())
def test__EXPIRE_GRACE_PERIOD_CONVERSION__put_converter(input_value):
    """
    Tests whether `EXPIRE_GRACE_PERIOD_CONVERSION.put_converter` works as intended.
    
    Parameters
    ----------
    input_value : `int`
        Processed value.
    
    Returns
    -------
    output : `int`
    """
    return EXPIRE_GRACE_PERIOD_CONVERSION.put_converter(input_value)
