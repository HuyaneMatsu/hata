import vampytest

from ...interaction_metadata import InteractionMetadataBase

from ..preinstanced import InteractionType


def test__InteractionType__name():
    """
    Tests whether ``InteractionType`` instance names are all strings.
    """
    for instance in InteractionType.INSTANCES.values():
        vampytest.assert_instance(instance.name, str)


def test__InteractionType__value():
    """
    Tests whether ``InteractionType`` instance values are all the expected value type.
    """
    for instance in InteractionType.INSTANCES.values():
        vampytest.assert_instance(instance.value, InteractionType.VALUE_TYPE)


def test__InteractionType__metadata_type():
    """
    Tests whether ``InteractionType`` instance metadata types are all metadata types.
    """
    for instance in InteractionType.INSTANCES.values():
        vampytest.assert_subtype(instance.metadata_type, InteractionMetadataBase)
