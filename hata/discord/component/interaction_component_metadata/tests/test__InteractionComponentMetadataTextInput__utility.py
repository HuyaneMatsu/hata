import vampytest

from ...component import ComponentType

from ..text_input import InteractionComponentMetadataTextInput

from .test__InteractionComponentMetadataTextInput__constructor import _assert_fields_set


def test__InteractionComponentMetadataTextInput__copy():
    """
    Tests whether ``InteractionComponentMetadataTextInput.copy`` works as intended.
    """
    custom_id = 'koishi'
    value = 'smart'
    
    interaction_component_metadata = InteractionComponentMetadataTextInput(
        custom_id = custom_id,
        value = value,
    )
    
    copy = interaction_component_metadata.copy()
    _assert_fields_set(copy)
    
    vampytest.assert_is_not(copy, interaction_component_metadata)
    vampytest.assert_eq(copy, interaction_component_metadata)


def test__InteractionComponentMetadataTextInput__copy_with__no_fields():
    """
    Tests whether ``InteractionComponentMetadataTextInput.copy_with`` works as intended.
    
    Case: no fields given.
    """
    custom_id = 'koishi'
    value = 'smart'
    
    interaction_component_metadata = InteractionComponentMetadataTextInput(
        custom_id = custom_id,
        value = value,
    )
    
    copy = interaction_component_metadata.copy_with()
    _assert_fields_set(copy)
    
    vampytest.assert_is_not(copy, interaction_component_metadata)
    vampytest.assert_eq(copy, interaction_component_metadata)


def test__InteractionComponentMetadataTextInput__copy_with__all_fields():
    """
    Tests whether ``InteractionComponentMetadataTextInput.copy_with`` works as intended.
    
    Case: all fields given.
    """
    old_custom_id = 'koishi'
    old_value = 'smart'
    
    new_custom_id = 'satori'
    new_value = 'smug'
    
    interaction_component_metadata = InteractionComponentMetadataTextInput(
        custom_id = old_custom_id,
        value = old_value,
    )
    
    copy = interaction_component_metadata.copy_with(
        custom_id = new_custom_id,
        value = new_value,
    )
    _assert_fields_set(copy)
    
    vampytest.assert_is_not(copy, interaction_component_metadata)
    vampytest.assert_ne(copy, interaction_component_metadata)
    
    vampytest.assert_eq(copy.custom_id, new_custom_id)
    vampytest.assert_eq(copy.value, new_value)


def test__InteractionComponentMetadataTextInput__copy_with_keyword_parameters__no_fields():
    """
    Tests whether ``InteractionComponentMetadataTextInput.copy_with_keyword_parameters`` works as intended.
    
    Case: no fields given.
    """
    custom_id = 'koishi'
    value = 'smart'
    
    interaction_component_metadata = InteractionComponentMetadataTextInput(
        custom_id = custom_id,
        value = value,
    )
    
    copy = interaction_component_metadata.copy_with_keyword_parameters({})
    _assert_fields_set(copy)
    
    vampytest.assert_is_not(copy, interaction_component_metadata)
    vampytest.assert_eq(copy, interaction_component_metadata)


def test__InteractionComponentMetadataTextInput__copy_with_keyword_parameters__all_fields():
    """
    Tests whether ``InteractionComponentMetadataTextInput.copy_with_keyword_parameters`` works as intended.
    
    Case: all fields given.
    """
    old_custom_id = 'koishi'
    old_value = 'smart'
    
    new_custom_id = 'satori'
    new_value = 'smug'
    
    interaction_component_metadata = InteractionComponentMetadataTextInput(
        custom_id = old_custom_id,
        value = old_value,
    )
    
    copy = interaction_component_metadata.copy_with_keyword_parameters({
        'custom_id': new_custom_id,
        'value': new_value,
    })
    _assert_fields_set(copy)
    
    vampytest.assert_is_not(copy, interaction_component_metadata)
    vampytest.assert_ne(copy, interaction_component_metadata)
    
    vampytest.assert_eq(copy.custom_id, new_custom_id)
    vampytest.assert_eq(copy.value, new_value)


def _iter_options__iter_custom_ids_and_values():
    yield (
        {},
        [],
    )
    
    yield (
        {
            'custom_id': 'koishi',
            'value': 'smart',
        },
        [
            (
                'koishi',
                ComponentType.text_input,
                'smart',
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options__iter_custom_ids_and_values()).returning_last())
def test__InteractionComponentMetadataTextInput__iter_custom_ids_and_values(keyword_parameters):
    """
    Tests whether ``InteractionComponentMetadataTextInput.iter_custom_ids_and_values`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `list<(str, ComponentType, None | str | tuple<str>)>`
    """
    interaction_component_metadata = InteractionComponentMetadataTextInput(**keyword_parameters)
    
    return [*interaction_component_metadata.iter_custom_ids_and_values()]
