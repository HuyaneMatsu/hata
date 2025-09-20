import vampytest

from ..base import InteractionMetadataBase

from .test__InteractionMetadataBase__constructor import _assert_fields_set


def test__InteractionMetadataBase__copy():
    """
    Tests whether ``InteractionMetadataBase.copy`` works as intended.
    """
    interaction_metadata = InteractionMetadataBase()
    copy = interaction_metadata.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, interaction_metadata)
    vampytest.assert_eq(copy, interaction_metadata)


def test__InteractionMetadataBase__copy_with__no_fields():
    """
    Tests whether ``InteractionMetadataBase.copy_with`` works as intended.
    
    Case: No fields given.
    """
    interaction_metadata = InteractionMetadataBase()
    copy = interaction_metadata.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, interaction_metadata)
    vampytest.assert_eq(copy, interaction_metadata)


def test__InteractionMetadataBase__copy_with_keyword_parameters__no_fields():
    """
    Tests whether ``InteractionMetadataBase.copy_with_keyword_parameters`` works as intended.
    
    Case: No fields given.
    """
    interaction_metadata = InteractionMetadataBase()
    copy = interaction_metadata.copy_with_keyword_parameters({})
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, interaction_metadata)
    vampytest.assert_eq(copy, interaction_metadata)
