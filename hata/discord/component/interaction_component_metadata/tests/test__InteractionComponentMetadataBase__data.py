import vampytest

from ..base import InteractionComponentMetadataBase

from .test__InteractionComponentMetadataBase__constructor import _assert_fields_set


def test__InteractionComponentMetadataBase__from_data():
    """
    Tests whether ``InteractionComponentMetadataBase.from_data`` works as intended.
    """
    data = {}
    
    interaction_component_metadata = InteractionComponentMetadataBase.from_data(data)
    _assert_fields_set(interaction_component_metadata)


def test__InteractionComponentMetadataBase__to_data():
    """
    Tests whether ``InteractionComponentMetadataBase.to_data`` works as intended.
    
    Case: include defaults.
    """
    interaction_component_metadata = InteractionComponentMetadataBase()
    
    vampytest.assert_eq(
        interaction_component_metadata.to_data(
            defaults = True,
        ),
        {},
    )
