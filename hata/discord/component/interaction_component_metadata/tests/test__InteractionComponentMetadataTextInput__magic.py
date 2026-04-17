import vampytest

from ...component_metadata import ComponentMetadataTextInput

from ..text_input import InteractionComponentMetadataTextInput


def test__InteractionComponentMetadataTextInput__repr():
    """
    Tests whether ``InteractionComponentMetadataTextInput.__repr__`` works as intended.
    """
    custom_id = 'koishi'
    value = 'smart'
    
    interaction_component_metadata = InteractionComponentMetadataTextInput(
        custom_id = custom_id,
        value = value,
    )
    
    output = repr(interaction_component_metadata)
    vampytest.assert_instance(output, str)


def test__InteractionComponentMetadataTextInput__hash():
    """
    Tests whether ``InteractionComponentMetadataTextInput.__hash__`` works as intended.
    """
    custom_id = 'koishi'
    value = 'smart'
    
    interaction_component_metadata = InteractionComponentMetadataTextInput(
        custom_id = custom_id,
        value = value,
    )
    
    output = hash(interaction_component_metadata)
    vampytest.assert_instance(output, int)


def test__InteractionComponentMetadataTextInput__eq__different_type():
    """
    Tests whether ``InteractionComponentMetadataTextInput.__eq__`` works as intended.
    
    Case: different type.
    """
    interaction_component_metadata = InteractionComponentMetadataTextInput()
    
    vampytest.assert_ne(interaction_component_metadata, object())


def _iter_options__eq():
    custom_id = 'koishi'
    value = 'smart'
    
    keyword_parameters = {
        'custom_id': custom_id,
        'value': value,
    }
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'custom_id': 'satori'
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'value': 'smug'
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__InteractionComponentMetadataTextInput__eq__same_type(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``InteractionComponentMetadataTextInput.__eq__`` works as intended.
    
    Case: same type.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create from.
    
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance from.
    
    Returns
    -------
    output : `bool`
    """
    interaction_component_metadata_0 = InteractionComponentMetadataTextInput(**keyword_parameters_0)
    interaction_component_metadata_1 = InteractionComponentMetadataTextInput(**keyword_parameters_1)
    
    output = interaction_component_metadata_0 == interaction_component_metadata_1
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__match_to_component():
    yield (
        {
            'custom_id': 'shrimp'
        },
        ComponentMetadataTextInput(
            custom_id = 'shrimp',
        ),
        True,
    )
    yield (
        {
            'custom_id': 'shrimp'
        },
        ComponentMetadataTextInput(
            custom_id = 'fry',
        ),
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__match_to_component()).returning_last())
def test__InteractionComponentMetadataTextInput__match_to_component(keyword_parameters, component_metadata):
    """
    Tests whether ``InteractionComponentMetadataTextInput._match_to_component`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create instance with.
    
    component_metadata : ``ComponentMetadataBase``
        Component metadata to test with.
    
    Returns
    -------
    output : `bool`
    """
    interaction_component_metadata = InteractionComponentMetadataTextInput(**keyword_parameters)
    
    output = interaction_component_metadata._match_to_component(component_metadata)
    vampytest.assert_instance(output, bool)
    return output
