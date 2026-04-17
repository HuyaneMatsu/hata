import vampytest

from ..base import InteractionComponentMetadataBase

from .test__InteractionComponentMetadataBase__constructor import _assert_fields_set


def test__InteractionComponentMetadataBase__copy():
    """
    Tests whether ``InteractionComponentMetadataBase.copy`` works as intended.
    """
    interaction_component_metadata = InteractionComponentMetadataBase()
    
    copy = interaction_component_metadata.copy()
    _assert_fields_set(copy)
    
    vampytest.assert_is_not(copy, interaction_component_metadata)
    vampytest.assert_eq(copy, interaction_component_metadata)


def test__InteractionComponentMetadataBase__copy_with__no_fields():
    """
    Tests whether ``InteractionComponentMetadataBase.copy_with`` works as intended.
    
    Case: no fields given.
    """
    interaction_component_metadata = InteractionComponentMetadataBase()
    
    copy = interaction_component_metadata.copy_with()
    _assert_fields_set(copy)
    
    vampytest.assert_is_not(copy, interaction_component_metadata)
    vampytest.assert_eq(copy, interaction_component_metadata)


def test__InteractionComponentMetadataBase__copy_with_keyword_parameters__no_fields():
    """
    Tests whether ``InteractionComponentMetadataBase.copy_with_keyword_parameters`` works as intended.
    
    Case: no fields given.
    """
    interaction_component_metadata = InteractionComponentMetadataBase()
    
    copy = interaction_component_metadata.copy_with_keyword_parameters({})
    _assert_fields_set(copy)
    
    vampytest.assert_is_not(copy, interaction_component_metadata)
    vampytest.assert_eq(copy, interaction_component_metadata)


def _iter_options__iter_custom_ids_and_values():
    yield (
        {},
        [],
    )


@vampytest._(vampytest.call_from(_iter_options__iter_custom_ids_and_values()).returning_last())
def test__InteractionComponentMetadataBase__iter_custom_ids_and_values(keyword_parameters):
    """
    Tests whether ``InteractionComponentMetadataBase.iter_custom_ids_and_values`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `list<(str, ComponentType, None | str | tuple<str>)>`
    """
    interaction_component_metadata = InteractionComponentMetadataBase(**keyword_parameters)
    
    return [*interaction_component_metadata.iter_custom_ids_and_values()]
