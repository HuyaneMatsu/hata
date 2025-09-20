import vampytest

from ...component import ComponentType

from ..string_select import InteractionComponentMetadataStringSelect

from .test__InteractionComponentMetadataStringSelect__constructor import _assert_fields_set


def test__InteractionComponentMetadataStringSelect__copy():
    """
    Tests whether ``InteractionComponentMetadataStringSelect.copy`` works as intended.
    """
    custom_id = 'koishi'
    values = ['oh', 'smart']
    
    interaction_component_metadata = InteractionComponentMetadataStringSelect(
        custom_id = custom_id,
        values = values,
    )
    
    copy = interaction_component_metadata.copy()
    _assert_fields_set(copy)
    
    vampytest.assert_is_not(copy, interaction_component_metadata)
    vampytest.assert_eq(copy, interaction_component_metadata)


def test__InteractionComponentMetadataStringSelect__copy_with__no_fields():
    """
    Tests whether ``InteractionComponentMetadataStringSelect.copy_with`` works as intended.
    
    Case: no fields given.
    """
    custom_id = 'koishi'
    values = ['oh', 'smart']
    
    interaction_component_metadata = InteractionComponentMetadataStringSelect(
        custom_id = custom_id,
        values = values,
    )
    
    copy = interaction_component_metadata.copy_with()
    _assert_fields_set(copy)
    
    vampytest.assert_is_not(copy, interaction_component_metadata)
    vampytest.assert_eq(copy, interaction_component_metadata)


def test__InteractionComponentMetadataStringSelect__copy_with__all_fields():
    """
    Tests whether ``InteractionComponentMetadataStringSelect.copy_with`` works as intended.
    
    Case: all fields given.
    """
    old_custom_id = 'koishi'
    old_values = ['oh', 'smart']
    
    new_custom_id = 'satori'
    new_values = ['blush', 'smug']
    
    interaction_component_metadata = InteractionComponentMetadataStringSelect(
        custom_id = old_custom_id,
        values = old_values,
    )
    
    copy = interaction_component_metadata.copy_with(
        custom_id = new_custom_id,
        values = new_values,
    )
    _assert_fields_set(copy)
    
    vampytest.assert_is_not(copy, interaction_component_metadata)
    vampytest.assert_ne(copy, interaction_component_metadata)
    
    vampytest.assert_eq(copy.custom_id, new_custom_id)
    vampytest.assert_eq(copy.values, tuple(new_values))


def test__InteractionComponentMetadataStringSelect__copy_with_keyword_parameters__no_fields():
    """
    Tests whether ``InteractionComponentMetadataStringSelect.copy_with_keyword_parameters`` works as intended.
    
    Case: no fields given.
    """
    custom_id = 'koishi'
    values = ['oh', 'smart']
    
    interaction_component_metadata = InteractionComponentMetadataStringSelect(
        custom_id = custom_id,
        values = values,
    )
    
    copy = interaction_component_metadata.copy_with_keyword_parameters({})
    _assert_fields_set(copy)
    
    vampytest.assert_is_not(copy, interaction_component_metadata)
    vampytest.assert_eq(copy, interaction_component_metadata)


def test__InteractionComponentMetadataStringSelect__copy_with_keyword_parameters__all_fields():
    """
    Tests whether ``InteractionComponentMetadataStringSelect.copy_with_keyword_parameters`` works as intended.
    
    Case: all fields given.
    """
    old_custom_id = 'koishi'
    old_values = ['oh', 'smart']
    
    new_custom_id = 'satori'
    new_values = ['blush', 'smug']
    
    interaction_component_metadata = InteractionComponentMetadataStringSelect(
        custom_id = old_custom_id,
        values = old_values,
    )
    
    copy = interaction_component_metadata.copy_with_keyword_parameters({
        'custom_id': new_custom_id,
        'values': new_values,
    })
    _assert_fields_set(copy)
    
    vampytest.assert_is_not(copy, interaction_component_metadata)
    vampytest.assert_ne(copy, interaction_component_metadata)
    
    vampytest.assert_eq(copy.custom_id, new_custom_id)
    vampytest.assert_eq(copy.values, tuple(new_values))


def _iter_options__iter_custom_ids_and_values():
    yield (
        {},
        [],
    )
    
    yield (
        {
            'custom_id': 'koishi',
            'values': ['oh', 'smart'],
        },
        [
            (
                'koishi',
                ComponentType.string_select,
                ('oh', 'smart'),
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options__iter_custom_ids_and_values()).returning_last())
def test__InteractionComponentMetadataStringSelect__iter_custom_ids_and_values(keyword_parameters):
    """
    Tests whether ``InteractionComponentMetadataStringSelect.iter_custom_ids_and_values`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `list<(str, ComponentType, None | str | tuple<str>)>`
    """
    interaction_component_metadata = InteractionComponentMetadataStringSelect(**keyword_parameters)
    
    return [*interaction_component_metadata.iter_custom_ids_and_values()]
