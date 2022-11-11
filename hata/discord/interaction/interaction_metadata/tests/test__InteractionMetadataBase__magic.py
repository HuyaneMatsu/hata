import vampytest

from ..base import InteractionMetadataBase


def test__InteractionMetadataBase__repr():
    """
    Tests whether ``InteractionMetadataBase.__repr__`` works as intended.
    """
    interaction_metadata = InteractionMetadataBase()
    vampytest.assert_instance(repr(interaction_metadata), str)


def test__InteractionMetadataBase__hash():
    """
    Tests whether ``InteractionMetadataBase.__hash__`` works as intended.
    """
    interaction_metadata = InteractionMetadataBase()
    vampytest.assert_instance(hash(interaction_metadata), int)


def test__InteractionMetadataBase__eq():
    """
    Tests whether ``InteractionMetadataBase.__eq__`` works as intended.
    """
    keyword_parameters = {}
    
    interaction_metadata = InteractionMetadataBase(**keyword_parameters)
    
    vampytest.assert_eq(interaction_metadata, interaction_metadata)
    vampytest.assert_ne(interaction_metadata, object())
    
    for field_name, field_value in (
    ):
        test_interaction_metadata = InteractionMetadataBase(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(interaction_metadata, test_interaction_metadata)
