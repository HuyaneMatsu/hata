import vampytest

from ..base import InteractionMetadataBase


def _check_is_all_field_set(interaction_metadata):
    """
    Checks whether all fields of the given interaction metadata are set.
    
    Parameters
    ----------
    interaction_metadata : ``InteractionMetadataBase``
        The interaction metadata to check.
    """
    vampytest.assert_instance(interaction_metadata, InteractionMetadataBase)


def test__InteractionMetadataBase__new__0():
    """
    Tests whether ``InteractionMetadataBase.__new__`` works as intended.
    
    Case: No fields given.
    """
    interaction_metadata = InteractionMetadataBase()
    _check_is_all_field_set(interaction_metadata)


def test__InteractionMetadataBase__create_empty():
    """
    Tests whether ``InteractionMetadataBase._create_empty`` works as intended.
    """
    interaction_metadata = InteractionMetadataBase._create_empty()
    _check_is_all_field_set(interaction_metadata)
