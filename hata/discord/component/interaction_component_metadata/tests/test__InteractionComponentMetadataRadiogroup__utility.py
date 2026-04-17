import vampytest

from ...component import ComponentType

from ..radio_group import InteractionComponentMetadataRadioGroup


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
                ComponentType.radio_group,
                'smart',
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options__iter_custom_ids_and_values()).returning_last())
def test__InteractionComponentMetadataRadioGroup__iter_custom_ids_and_values(keyword_parameters):
    """
    Tests whether ``InteractionComponentMetadataRadioGroup.iter_custom_ids_and_values`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `list<(str, ComponentType, None | str | tuple<str>)>`
    """
    interaction_component_metadata = InteractionComponentMetadataRadioGroup(**keyword_parameters)
    
    return [*interaction_component_metadata.iter_custom_ids_and_values()]
