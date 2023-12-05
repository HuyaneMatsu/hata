import vampytest

from ...interaction_metadata import InteractionMetadataBase

from ..preinstanced import InteractionType


@vampytest.call_from(InteractionType.INSTANCES.values())
def test__InteractionType__instances(instance):
    """
    Tests whether ``InteractionType`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``InteractionType``
        The instance to test.
    """
    vampytest.assert_instance(instance, InteractionType)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, InteractionType.VALUE_TYPE)
    vampytest.assert_subtype(instance.metadata_type, InteractionMetadataBase)
