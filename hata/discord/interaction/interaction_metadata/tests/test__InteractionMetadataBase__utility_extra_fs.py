import vampytest

from ..base import InteractionMetadataBase


def test__InteractionMetadataBase__iter_components():
    """
    Tests whether ``InteractionMetadataBase.iter_components`` works as intended.
    """
    interaction_metadata = InteractionMetadataBase()
    
    vampytest.assert_eq([*interaction_metadata.iter_components()], [])


def test__InteractionMetadataBase__iter_custom_ids_and_values():
    """
    Tests whether ``InteractionMetadataBase.iter_custom_ids_and_values`` works as intended.
    """
    interaction_metadata = InteractionMetadataBase()
    
    vampytest.assert_eq(dict(interaction_metadata.iter_custom_ids_and_values()), {})


def test__InteractionMetadataBase__get_custom_id_value_relation():
    """
    Tests whether ``InteractionMetadataBase.get_custom_id_value_relation`` works as intended.
    """
    interaction_metadata = InteractionMetadataBase()
    
    vampytest.assert_eq(interaction_metadata.get_custom_id_value_relation(), {})



def test__InteractionMetadataBase__get_value_for():
    """
    Tests whether ``InteractionMetadataBase.get_value_for`` works as intended.
    """
    interaction_metadata = InteractionMetadataBase()
    
    vampytest.assert_is(interaction_metadata.get_value_for('Ran'), None)


def test__InteractionMetadataBase__get_match_and_value():
    """
    Tests whether ``InteractionMetadataBase.get_match_and_value`` works as intended.
    """
    interaction_metadata = InteractionMetadataBase()
    
    vampytest.assert_eq(
        interaction_metadata.get_match_and_value(lambda custom_id: 'Ran' if custom_id == 'custom_id' else None),
        (None, None)
    )


def test__InteractionMetadataBase__iter_matches_and_values():
    """
    Tests whether ``InteractionMetadataBase.iter_matches_and_values`` works as intended.
    """
    interaction_metadata = InteractionMetadataBase()
    
    vampytest.assert_eq(
        [*interaction_metadata.iter_matches_and_values(lambda custom_id: 'Ran' if custom_id == 'custom_id' else None)],
        [],
    )
