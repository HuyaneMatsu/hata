import vampytest

from .. import SKUFeatureType


def test__SKUFeatureType__name():
    """
    Tests whether ``SKUFeatureType`` instance names are all strings.
    """
    for instance in SKUFeatureType.INSTANCES.values():
        vampytest.assert_instance(instance.name, str)


def test__SKUFeatureType__value():
    """
    Tests whether ``SKUFeatureType`` instance values are all the expected value type.
    """
    for instance in SKUFeatureType.INSTANCES.values():
        vampytest.assert_instance(instance.value, SKUFeatureType.VALUE_TYPE)
