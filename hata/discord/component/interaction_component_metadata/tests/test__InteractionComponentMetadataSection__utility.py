import vampytest

from ...component import ComponentType
from ...interaction_component import InteractionComponent

from ..section import InteractionComponentMetadataSection

from .test__InteractionComponentMetadataSection__constructor import _assert_fields_set


def test__InteractionComponentMetadataSection__copy():
    """
    Tests whether ``InteractionComponentMetadataSection.copy`` works as intended.
    """
    interaction_components = [
        InteractionComponent(
            ComponentType.text_display,
        ),
        InteractionComponent(
            ComponentType.text_display,
        ),
    ]
    
    thumbnail = InteractionComponent(
        ComponentType.button,
        custom_id = 'alice',
    )
    
    interaction_component_metadata = InteractionComponentMetadataSection(
        components = interaction_components,
        thumbnail = thumbnail,
    )
    
    copy = interaction_component_metadata.copy()
    _assert_fields_set(copy)
    
    vampytest.assert_is_not(copy, interaction_component_metadata)
    vampytest.assert_eq(copy, interaction_component_metadata)


def test__InteractionComponentMetadataSection__copy_with__no_fields():
    """
    Tests whether ``InteractionComponentMetadataSection.copy_with`` works as intended.
    
    Case: no fields given.
    """
    interaction_components = [
        InteractionComponent(
            ComponentType.text_display,
        ),
        InteractionComponent(
            ComponentType.text_display,
        ),
    ]
    
    thumbnail = InteractionComponent(
        ComponentType.button,
        custom_id = 'alice',
    )
    
    interaction_component_metadata = InteractionComponentMetadataSection(
        components = interaction_components,
        thumbnail = thumbnail,
    )
    
    copy = interaction_component_metadata.copy_with()
    _assert_fields_set(copy)
    
    vampytest.assert_is_not(copy, interaction_component_metadata)
    vampytest.assert_eq(copy, interaction_component_metadata)


def test__InteractionComponentMetadataSection__copy_with__all_fields():
    """
    Tests whether ``InteractionComponentMetadataSection.copy_with`` works as intended.
    
    Case: all fields given.
    """
    old_interaction_components = [
        InteractionComponent(
            ComponentType.text_display,
        ),
        InteractionComponent(
            ComponentType.text_display,
        ),
    ]
    
    old_thumbnail = InteractionComponent(
        ComponentType.button,
        custom_id = 'alice',
    )
    
    new_interaction_components = [
        InteractionComponent(
            ComponentType.text_display,
        ),
    ]
    
    new_thumbnail = InteractionComponent(
        ComponentType.button,
        custom_id = 'marisa',
    )
    
    interaction_component_metadata = InteractionComponentMetadataSection(
        components = old_interaction_components,
        thumbnail = old_thumbnail,
    )
    
    copy = interaction_component_metadata.copy_with(
        components = new_interaction_components,
        thumbnail = new_thumbnail,
    )
    _assert_fields_set(copy)
    
    vampytest.assert_is_not(copy, interaction_component_metadata)
    vampytest.assert_ne(copy, interaction_component_metadata)
    
    vampytest.assert_eq(copy.components, tuple(new_interaction_components))
    vampytest.assert_eq(copy.thumbnail, new_thumbnail)


def test__InteractionComponentMetadataSection__copy_with_keyword_parameters__no_fields():
    """
    Tests whether ``InteractionComponentMetadataSection.copy_with_keyword_parameters`` works as intended.
    
    Case: no fields given.
    """
    interaction_components = [
        InteractionComponent(
            ComponentType.text_display,
        ),
        InteractionComponent(
            ComponentType.text_display,
        ),
    ]
    
    thumbnail = InteractionComponent(
        ComponentType.button,
        custom_id = 'alice',
    )
    
    interaction_component_metadata = InteractionComponentMetadataSection(
        components = interaction_components,
        thumbnail = thumbnail,
    )
    
    copy = interaction_component_metadata.copy_with_keyword_parameters({})
    _assert_fields_set(copy)
    
    vampytest.assert_is_not(copy, interaction_component_metadata)
    vampytest.assert_eq(copy, interaction_component_metadata)


def test__InteractionComponentMetadataSection__copy_with_keyword_parameters__all_fields():
    """
    Tests whether ``InteractionComponentMetadataSection.copy_with_keyword_parameters`` works as intended.
    
    Case: all fields given.
    """
    old_interaction_components = [
        InteractionComponent(
            ComponentType.text_display,
        ),
        InteractionComponent(
            ComponentType.text_display,
        ),
    ]
    
    old_thumbnail = InteractionComponent(
        ComponentType.button,
        custom_id = 'alice',
    )
    
    new_interaction_components = [
        InteractionComponent(
            ComponentType.text_display,
        ),
    ]
    
    new_thumbnail = InteractionComponent(
        ComponentType.button,
        custom_id = 'marisa',
    )
    
    interaction_component_metadata = InteractionComponentMetadataSection(
        components = old_interaction_components,
        thumbnail = old_thumbnail,
    )
    
    copy = interaction_component_metadata.copy_with_keyword_parameters({
        'components': new_interaction_components,
        'thumbnail': new_thumbnail,
    })
    _assert_fields_set(copy)
    
    vampytest.assert_is_not(copy, interaction_component_metadata)
    vampytest.assert_ne(copy, interaction_component_metadata)
    
    vampytest.assert_eq(copy.components, tuple(new_interaction_components))
    vampytest.assert_eq(copy.thumbnail, new_thumbnail)


def _iter_options__iter_custom_ids_and_values():
    yield (
        {},
        [],
    )
    
    yield (
        {
            'components': [
                InteractionComponent(
                    ComponentType.text_display,
                ),
                InteractionComponent(
                    ComponentType.text_display,
                ),
            ],
            'thumbnail': 
                InteractionComponent(
                    ComponentType.button,
                    custom_id = 'alice',
                ),
        },
        [
            (
                'alice',
                ComponentType.button,
                None,
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options__iter_custom_ids_and_values()).returning_last())
def test__InteractionComponentMetadataSection__iter_custom_ids_and_values(keyword_parameters):
    """
    Tests whether ``InteractionComponentMetadataSection.iter_custom_ids_and_values`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `list<(str, ComponentType, None | str | tuple<str>)>`
    """
    interaction_component_metadata = InteractionComponentMetadataSection(**keyword_parameters)
    
    return [*interaction_component_metadata.iter_custom_ids_and_values()]
