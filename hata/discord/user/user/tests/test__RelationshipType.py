import vampytest

from ..preinstanced import RelationshipType


def test__RelationshipType__name():
    """
    Tests whether ``RelationshipType`` instance names are all strings.
    """
    for instance in RelationshipType.INSTANCES.values():
        vampytest.assert_instance(instance.name, str)


def test__RelationshipType__value():
    """
    Tests whether ``RelationshipType`` instance values are all the expected value type.
    """
    for instance in RelationshipType.INSTANCES.values():
        vampytest.assert_instance(instance.value, RelationshipType.VALUE_TYPE)
