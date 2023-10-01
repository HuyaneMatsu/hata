import vampytest

from ..preinstanced import SKUFeature


def test__SKUFeature__name():
    """
    Tests whether ``SKUFeature`` instance names are all strings.
    """
    for instance in SKUFeature.INSTANCES.values():
        vampytest.assert_instance(instance.name, str)


def test__SKUFeature__value():
    """
    Tests whether ``SKUFeature`` instance values are all the expected value type.
    """
    for instance in SKUFeature.INSTANCES.values():
        vampytest.assert_instance(instance.value, SKUFeature.VALUE_TYPE)
