import vampytest

from ...interaction_option import InteractionOption

from ..application_command_autocomplete import InteractionMetadataBase


def _iter_options__iter_options():
    yield (
        {},
        [],
    )


@vampytest._(vampytest.call_from(_iter_options__iter_options()).returning_last())
def test__InteractionMetadataBase__iter_options(keyword_parameters):
    """
    Tests whether ``InteractionMetadataBase.iter_options`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : ``list<InteractionOption>``
    """
    interaction_metadata = InteractionMetadataBase(**keyword_parameters)
    
    output = [*interaction_metadata.iter_options()]
    
    for element in output:
        vampytest.assert_instance(element, InteractionOption)
    
    return output


def _iter_options__focused_option():
    yield (
        {},
        None,
    )
    

@vampytest._(vampytest.call_from(_iter_options__focused_option()).returning_last())
def test__InteractionMetadataBase__focused_option(keyword_parameters):
    """
    Tests whether ``InteractionMetadataBase.focused_option`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : ``None | InteractionOption``
    """
    interaction_metadata = InteractionMetadataBase(**keyword_parameters)
    
    output = interaction_metadata.focused_option
    vampytest.assert_instance(output, InteractionOption, nullable = True)
    return output


def _iter_options__get_non_focused_values():
    yield (
        {},
        {},
    )


@vampytest._(vampytest.call_from(_iter_options__get_non_focused_values()).returning_last())
def test__InteractionMetadataBase__get_non_focused_values(keyword_parameters):
    """
    Tests whether ``InteractionMetadataBase.get_non_focused_values`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `dict<str, None | str>`
    """
    interaction_metadata = InteractionMetadataBase(**keyword_parameters)
    
    output = interaction_metadata.get_non_focused_values()
    
    vampytest.assert_instance(output, dict)
    for key, value in output.items():
        vampytest.assert_instance(key, str)
        vampytest.assert_instance(value, str, nullable = True)
    
    return output


def _iter_options__get_value_of():
    yield (
        {},
        (
            'koishi',
        ),
        None,
    )


@vampytest._(vampytest.call_from(_iter_options__get_value_of()).returning_last())
def test__InteractionMetadataBase__get_value_of(keyword_parameters, option_names):
    """
    Tests whether ``InteractionMetadataBase.get_value_of`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create instance with.
    
    option_names : `tuple<str>`
        Option names to get value for.
    
    Returns
    -------
    output : `None | str`
    """
    interaction_metadata = InteractionMetadataBase(**keyword_parameters)
    output = interaction_metadata.get_value_of(*option_names)
    vampytest.assert_instance(output, str, nullable = True)
    return output
