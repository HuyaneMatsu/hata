import vampytest

from ....component import ComponentType, InteractionComponent

from ..message_component import InteractionMetadataMessageComponent


def _iter_options__iter_custom_ids_and_values():
    yield (
        {
            'component': InteractionComponent(
                ComponentType.string_select,
                custom_id = 'negative',
                values = ['kaenbyou', 'rin']
            ),
        },
        [
            ('negative', ComponentType.string_select, ('kaenbyou', 'rin')),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options__iter_custom_ids_and_values()).returning_last())
def test__InteractionMetadataMessageComponent__iter_custom_ids_and_values(keyword_parameters):
    """
    Tests whether ``InteractionMetadataMessageComponent.iter_custom_ids_and_values`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `list<(str, ComponentType, None | str | tuple<str>)>`
    """
    interaction_metadata = InteractionMetadataMessageComponent(**keyword_parameters)
    return [*interaction_metadata.iter_custom_ids_and_values()]
