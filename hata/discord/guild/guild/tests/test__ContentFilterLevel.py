import vampytest

from ..preinstanced import ContentFilterLevel


def test__ContentFilterLevel__name():
    """
    Tests whether ``ContentFilterLevel`` instance names are all strings.
    """
    for instance in ContentFilterLevel.INSTANCES.values():
        vampytest.assert_instance(instance.name, str)


def test__ContentFilterLevel__value():
    """
    Tests whether ``ContentFilterLevel`` instance values are all the expected value type.
    """
    for instance in ContentFilterLevel.INSTANCES.values():
        vampytest.assert_instance(instance.value, ContentFilterLevel.VALUE_TYPE)
