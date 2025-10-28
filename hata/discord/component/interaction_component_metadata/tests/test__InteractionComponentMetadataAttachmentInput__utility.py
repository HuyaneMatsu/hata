import vampytest

from ...component import ComponentType

from ..attachment_input import InteractionComponentMetadataAttachmentInput


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
                ComponentType.attachment_input,
                ('oh', 'smart'),
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options__iter_custom_ids_and_values()).returning_last())
def test__InteractionComponentMetadataAttachmentInput__iter_custom_ids_and_values(keyword_parameters):
    """
    Tests whether ``InteractionComponentMetadataAttachmentInput.iter_custom_ids_and_values`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `list<(str, ComponentType, None | str | tuple<str>)>`
    """
    interaction_component_metadata = InteractionComponentMetadataAttachmentInput(**keyword_parameters)
    
    return [*interaction_component_metadata.iter_custom_ids_and_values()]
