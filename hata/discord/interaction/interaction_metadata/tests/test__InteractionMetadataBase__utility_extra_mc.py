import vampytest

from ..base import InteractionMetadataBase


def test__InteractionMetadataBase__iter_values():
    """
    Tests whether ``InteractionMetadataBase.iter_values`` works as intended.
    """
    interaction_metadata = InteractionMetadataBase()
    
    vampytest.assert_eq([*interaction_metadata.iter_values()], [])


def test__InteractionMetadataBase__iter_entries():
    """
    Tests whether ``InteractionMetadataBase.iter_entities`` works as intended.
    """
    interaction_metadata = InteractionMetadataBase()
    
    vampytest.assert_eq([*interaction_metadata.iter_entities()], [])


def test__InteractionMetadataBase__entities():
    """
    Tests whether ``InteractionMetadataBase.entities`` works as intended.
    """
    interaction_metadata = InteractionMetadataBase()
    
    vampytest.assert_eq(interaction_metadata.entities, [])
