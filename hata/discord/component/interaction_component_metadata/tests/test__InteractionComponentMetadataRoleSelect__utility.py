import vampytest

from ...component import ComponentType

from ..role_select import InteractionComponentMetadataRoleSelect


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
                ComponentType.role_select,
                ('oh', 'smart'),
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options__iter_custom_ids_and_values()).returning_last())
def test__InteractionComponentMetadataRoleSelect__iter_custom_ids_and_values(keyword_parameters):
    """
    Tests whether ``InteractionComponentMetadataRoleSelect.iter_custom_ids_and_values`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `list<(str, ComponentType, None | str | tuple<str>)>`
    """
    interaction_component_metadata = InteractionComponentMetadataRoleSelect(**keyword_parameters)
    
    return [*interaction_component_metadata.iter_custom_ids_and_values()]
