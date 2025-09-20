import vampytest

from ....application_command import ApplicationCommandTargetType
from ....component import ComponentType, InteractionComponent

from ..base import InteractionMetadataBase


def test__InteractionMetadataBase__placeholders():
    """
    Tests whether ``InteractionMetadataBase``'s placeholders work as intended.
    """
    interaction_metadata = InteractionMetadataBase()
    
    vampytest.assert_instance(interaction_metadata.application_command_id, int)
    vampytest.assert_instance(interaction_metadata.application_command_name, str)
    vampytest.assert_instance(interaction_metadata.components, tuple, nullable = True)
    vampytest.assert_instance(interaction_metadata.component, InteractionComponent, nullable = True)
    vampytest.assert_instance(interaction_metadata.custom_id, str, nullable = True)
    vampytest.assert_instance(interaction_metadata.options, tuple, nullable = True)
    vampytest.assert_instance(interaction_metadata.target_id, int)
    vampytest.assert_instance(interaction_metadata.target_type, ApplicationCommandTargetType)
