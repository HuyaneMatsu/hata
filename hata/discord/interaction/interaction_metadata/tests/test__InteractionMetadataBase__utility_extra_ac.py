import vampytest

from ..base import InteractionMetadataBase


def test__InteractionMetadataBase__target():
    """
    Tests whether ``InteractionMetadataBase.target`` works as intended.
    """
    interaction_metadata = InteractionMetadataBase()
    
    vampytest.assert_is(interaction_metadata.target, None)
