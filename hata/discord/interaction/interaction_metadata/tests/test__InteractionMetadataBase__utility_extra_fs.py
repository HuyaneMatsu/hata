import vampytest

from ....component import InteractionComponent

from ..base import InteractionMetadataBase


def _iter_options__iter_components():
    yield (
        {},
        [],
    )


@vampytest._(vampytest.call_from(_iter_options__iter_components()).returning_last())
def test__InteractionMetadataBase__iter_components(keyword_parameters):
    """
    Tests whether ``InteractionMetadataBase.iter_components`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : ``list<InteractionComponent>``
    """
    interaction_metadata = InteractionMetadataBase(**keyword_parameters)
    
    output = [*interaction_metadata.iter_components()]
    
    for element in output:
        vampytest.assert_instance(element, InteractionComponent)
    
    return output


def _iter_options__iter_custom_ids_and_values():
    yield (
        {},
        [],
    )


@vampytest._(vampytest.call_from(_iter_options__iter_custom_ids_and_values()).returning_last())
def test__InteractionMetadataBase__iter_custom_ids_and_values(keyword_parameters):
    """
    Tests whether ``InteractionMetadataBase.iter_custom_ids_and_values`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `list<(str, ComponentType, None | str | tuple<str>)>`
    """
    interaction_metadata = InteractionMetadataBase(**keyword_parameters)
    return [*interaction_metadata.iter_custom_ids_and_values()]
