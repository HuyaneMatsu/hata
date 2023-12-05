import vampytest

from ..preinstanced import RelationshipType


@vampytest.call_from(RelationshipType.INSTANCES.values())
def test__RelationshipType__instances(instance):
    """
    Tests whether ``RelationshipType`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``RelationshipType``
        The instance to test.
    """
    vampytest.assert_instance(instance, RelationshipType)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, RelationshipType.VALUE_TYPE)
