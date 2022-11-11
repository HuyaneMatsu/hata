import vampytest

from ....component import ComponentType

from ...resolved import Resolved

from ..base import InteractionMetadataBase


def test__InteractionMetadataBase__placeholders():
    """
    Tests whether ``InteractionMetadataBase``'s placeholders work as intended.
    """
    interaction_metadata = InteractionMetadataBase()
    
    vampytest.assert_instance(interaction_metadata.component_type, ComponentType)
    vampytest.assert_instance(interaction_metadata.components, tuple, nullable = True)
    vampytest.assert_instance(interaction_metadata.custom_id, str, nullable = True)
    vampytest.assert_instance(interaction_metadata.id, int)
    vampytest.assert_instance(interaction_metadata.name, str)
    vampytest.assert_instance(interaction_metadata.options, tuple, nullable = True)
    vampytest.assert_instance(interaction_metadata.options, Resolved, nullable = True)
    vampytest.assert_instance(interaction_metadata.target_id, int)
    vampytest.assert_instance(interaction_metadata.components, tuple, nullable = True)
    vampytest.assert_instance(interaction_metadata.values, tuple, nullable = True)
