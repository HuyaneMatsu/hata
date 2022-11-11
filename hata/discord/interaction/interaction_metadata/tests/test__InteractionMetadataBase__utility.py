import vampytest

from ..base import InteractionMetadataBase

from .test__InteractionMetadataBase__constructor import _check_is_all_field_set


def test__InteractionMetadataBase__copy():
    """
    Tests whether ``InteractionMetadataBase.copy`` works as intended.
    """
    interaction_metadata = InteractionMetadataBase()
    copy = interaction_metadata.copy()
    _check_is_all_field_set(copy)
    vampytest.assert_is_not(copy, interaction_metadata)
    vampytest.assert_eq(copy, interaction_metadata)


def test__InteractionMetadataBase__copy_with__0():
    """
    Tests whether ``InteractionMetadataBase.copy_with`` works as intended.
    
    Case: No fields given.
    """
    interaction_metadata = InteractionMetadataBase()
    copy = interaction_metadata.copy_with()
    _check_is_all_field_set(copy)
    vampytest.assert_is_not(copy, interaction_metadata)
    vampytest.assert_eq(copy, interaction_metadata)
