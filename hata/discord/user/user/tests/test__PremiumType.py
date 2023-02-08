import vampytest

from ..preinstanced import PremiumType


def test__PremiumType__name():
    """
    Tests whether ``PremiumType`` instance names are all strings.
    """
    for instance in PremiumType.INSTANCES.values():
        vampytest.assert_instance(instance.name, str)


def test__PremiumType__value():
    """
    Tests whether ``PremiumType`` instance values are all the expected value type.
    """
    for instance in PremiumType.INSTANCES.values():
        vampytest.assert_instance(instance.value, PremiumType.VALUE_TYPE)
