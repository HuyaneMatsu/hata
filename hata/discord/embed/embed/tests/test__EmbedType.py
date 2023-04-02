import vampytest

from ..preinstanced import EmbedType


def test__EmbedType__name():
    """
    Tests whether ``EmbedType`` instance names are all strings.
    """
    for instance in EmbedType.INSTANCES.values():
        vampytest.assert_instance(instance.name, str)


def test__EmbedType__value():
    """
    Tests whether ``EmbedType`` instance values are all the expected value type.
    """
    for instance in EmbedType.INSTANCES.values():
        vampytest.assert_instance(instance.value, EmbedType.VALUE_TYPE)
