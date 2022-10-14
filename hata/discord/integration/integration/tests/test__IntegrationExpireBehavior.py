import vampytest

from .. import IntegrationExpireBehavior


def test__IntegrationExpireBehavior__name():
    """
    Tests whether ``IntegrationExpireBehavior`` instance names are all strings.
    """
    for instance in IntegrationExpireBehavior.INSTANCES.values():
        vampytest.assert_instance(instance.name, str)


def test__IntegrationExpireBehavior__value():
    """
    Tests whether ``IntegrationExpireBehavior`` instance values are all the expected value type.
    """
    for instance in IntegrationExpireBehavior.INSTANCES.values():
        vampytest.assert_instance(instance.value, IntegrationExpireBehavior.VALUE_TYPE)
