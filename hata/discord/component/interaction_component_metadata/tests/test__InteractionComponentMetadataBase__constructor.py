import vampytest

from ..base import InteractionComponentMetadataBase


def _assert_fields_set(interaction_component_metadata):
    """
    Checks whether the ``InteractionComponentMetadataBase`` has all it's attributes set.
    
    Parameters
    ----------
    interaction_component_metadata : ``InteractionComponentMetadataBase``
        Component metadata to check.
    """
    vampytest.assert_instance(interaction_component_metadata, InteractionComponentMetadataBase)


def test__InteractionComponentMetadataBase__new__no_fields():
    """
    Tests whether ``InteractionComponentMetadataBase.__new__`` works as intended.
    
    Case: no fields given.
    """
    interaction_component_metadata = InteractionComponentMetadataBase()
    _assert_fields_set(interaction_component_metadata)


def test__InteractionComponentMetadataBase__from_keyword_parameters__no_fields():
    """
    Tests whether ``InteractionComponentMetadataBase.from_keyword_parameters`` works as intended.
    
    Case: no fields given.
    """
    keyword_parameters = {}
    
    interaction_component_metadata = InteractionComponentMetadataBase.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(interaction_component_metadata)
