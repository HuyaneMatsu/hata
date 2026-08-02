import vampytest

from ...component import ComponentType

from ..checkbox import InteractionComponentMetadataCheckbox

from .test__InteractionComponentMetadataCheckbox__constructor import _assert_fields_set


def test__InteractionComponentMetadataCheckbox__copy():
    """
    Tests whether ``InteractionComponentMetadataCheckbox.copy`` works as intended.
    """
    custom_id = 'koishi'
    value = '\001'
    
    interaction_component_metadata = InteractionComponentMetadataCheckbox(
        custom_id = custom_id,
        value = value,
    )
    
    copy = interaction_component_metadata.copy()
    _assert_fields_set(copy)
    
    vampytest.assert_is_not(copy, interaction_component_metadata)
    vampytest.assert_eq(copy, interaction_component_metadata)


def test__InteractionComponentMetadataCheckbox__copy_with__no_fields():
    """
    Tests whether ``InteractionComponentMetadataCheckbox.copy_with`` works as intended.
    
    Case: no fields given.
    """
    custom_id = 'koishi'
    value = '\001'
    
    interaction_component_metadata = InteractionComponentMetadataCheckbox(
        custom_id = custom_id,
        value = value,
    )
    
    copy = interaction_component_metadata.copy_with()
    _assert_fields_set(copy)
    
    vampytest.assert_is_not(copy, interaction_component_metadata)
    vampytest.assert_eq(copy, interaction_component_metadata)


def test__InteractionComponentMetadataCheckbox__copy_with__all_fields():
    """
    Tests whether ``InteractionComponentMetadataCheckbox.copy_with`` works as intended.
    
    Case: all fields given.
    """
    old_custom_id = 'koishi'
    old_value = '\001'
    
    new_custom_id = 'satori'
    new_value = '\000'
    
    interaction_component_metadata = InteractionComponentMetadataCheckbox(
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


def test__InteractionComponentMetadataCheckbox__copy_with_keyword_parameters__no_fields():
    """
    Tests whether ``InteractionComponentMetadataCheckbox.copy_with_keyword_parameters`` works as intended.
    
    Case: no fields given.
    """
    custom_id = 'koishi'
    value = '\001'
    
    interaction_component_metadata = InteractionComponentMetadataCheckbox(
        custom_id = custom_id,
        value = value,
    )
    
    copy = interaction_component_metadata.copy_with_keyword_parameters({})
    _assert_fields_set(copy)
    
    vampytest.assert_is_not(copy, interaction_component_metadata)
    vampytest.assert_eq(copy, interaction_component_metadata)


def test__InteractionComponentMetadataCheckbox__copy_with_keyword_parameters__all_fields():
    """
    Tests whether ``InteractionComponentMetadataCheckbox.copy_with_keyword_parameters`` works as intended.
    
    Case: all fields given.
    """
    old_custom_id = 'koishi'
    old_value = '\001'
    
    new_custom_id = 'satori'
    new_value = '\000'
    
    interaction_component_metadata = InteractionComponentMetadataCheckbox(
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
            'value': '\001',
        },
        [
            (
                'koishi',
                ComponentType.checkbox,
                '\001',
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options__iter_custom_ids_and_values()).returning_last())
def test__InteractionComponentMetadataCheckbox__iter_custom_ids_and_values(keyword_parameters):
    """
    Tests whether ``InteractionComponentMetadataCheckbox.iter_custom_ids_and_values`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `list<(str, ComponentType, None | str | tuple<str>)>`
    """
    interaction_component_metadata = InteractionComponentMetadataCheckbox(**keyword_parameters)
    
    return [*interaction_component_metadata.iter_custom_ids_and_values()]
