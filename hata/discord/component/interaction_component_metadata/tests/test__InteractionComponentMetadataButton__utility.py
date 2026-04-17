import vampytest

from ...component import ComponentType

from ..button import InteractionComponentMetadataButton

from .test__InteractionComponentMetadataButton__constructor import _assert_fields_set


def test__InteractionComponentMetadataButton__copy():
    """
    Tests whether ``InteractionComponentMetadataButton.copy`` works as intended.
    """
    custom_id = 'koishi'
    
    interaction_component_metadata = InteractionComponentMetadataButton(
        custom_id = custom_id,
    )
    
    copy = interaction_component_metadata.copy()
    _assert_fields_set(copy)
    
    vampytest.assert_is_not(copy, interaction_component_metadata)
    vampytest.assert_eq(copy, interaction_component_metadata)


def test__InteractionComponentMetadataButton__copy_with__no_fields():
    """
    Tests whether ``InteractionComponentMetadataButton.copy_with`` works as intended.
    
    Case: no fields given.
    """
    custom_id = 'koishi'
    
    interaction_component_metadata = InteractionComponentMetadataButton(
        custom_id = custom_id,
    )
    
    copy = interaction_component_metadata.copy_with()
    _assert_fields_set(copy)
    
    vampytest.assert_is_not(copy, interaction_component_metadata)
    vampytest.assert_eq(copy, interaction_component_metadata)


def test__InteractionComponentMetadataButton__copy_with__all_fields():
    """
    Tests whether ``InteractionComponentMetadataButton.copy_with`` works as intended.
    
    Case: all fields given.
    """
    old_custom_id = 'koishi'
    
    new_custom_id = 'satori'
    
    interaction_component_metadata = InteractionComponentMetadataButton(
        custom_id = old_custom_id,
    )
    
    copy = interaction_component_metadata.copy_with(
        custom_id = new_custom_id,
    )
    _assert_fields_set(copy)
    
    vampytest.assert_is_not(copy, interaction_component_metadata)
    vampytest.assert_ne(copy, interaction_component_metadata)
    
    vampytest.assert_eq(copy.custom_id, new_custom_id)


def test__InteractionComponentMetadataButton__copy_with_keyword_parameters__no_fields():
    """
    Tests whether ``InteractionComponentMetadataButton.copy_with_keyword_parameters`` works as intended.
    
    Case: no fields given.
    """
    custom_id = 'koishi'
    
    interaction_component_metadata = InteractionComponentMetadataButton(
        custom_id = custom_id,
    )
    
    copy = interaction_component_metadata.copy_with_keyword_parameters({})
    _assert_fields_set(copy)
    
    vampytest.assert_is_not(copy, interaction_component_metadata)
    vampytest.assert_eq(copy, interaction_component_metadata)


def test__InteractionComponentMetadataButton__copy_with_keyword_parameters__all_fields():
    """
    Tests whether ``InteractionComponentMetadataButton.copy_with_keyword_parameters`` works as intended.
    
    Case: all fields given.
    """
    old_custom_id = 'koishi'
    
    new_custom_id = 'satori'
    
    interaction_component_metadata = InteractionComponentMetadataButton(
        custom_id = old_custom_id,
    )
    
    copy = interaction_component_metadata.copy_with_keyword_parameters({
        'custom_id': new_custom_id,
    })
    _assert_fields_set(copy)
    
    vampytest.assert_is_not(copy, interaction_component_metadata)
    vampytest.assert_ne(copy, interaction_component_metadata)
    
    vampytest.assert_eq(copy.custom_id, new_custom_id)


def _iter_options__iter_custom_ids_and_values():
    yield (
        {},
        [],
    )
    
    yield (
        {
            'custom_id': 'koishi',
        },
        [
            (
                'koishi',
                ComponentType.button,
                None,
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options__iter_custom_ids_and_values()).returning_last())
def test__InteractionComponentMetadataButton__iter_custom_ids_and_values(keyword_parameters):
    """
    Tests whether ``InteractionComponentMetadataButton.iter_custom_ids_and_values`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `list<(str, ComponentType, None | str | tuple<str>)>`
    """
    interaction_component_metadata = InteractionComponentMetadataButton(**keyword_parameters)
    
    return [*interaction_component_metadata.iter_custom_ids_and_values()]
