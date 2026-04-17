import vampytest

from ...component_metadata import ComponentMetadataButton

from ..button import InteractionComponentMetadataButton


def test__InteractionComponentMetadataButton__repr():
    """
    Tests whether ``InteractionComponentMetadataButton.__repr__`` works as intended.
    """
    custom_id = 'koishi'
    
    interaction_component_metadata = InteractionComponentMetadataButton(
        custom_id = custom_id,
    )
    
    output = repr(interaction_component_metadata)
    vampytest.assert_instance(output, str)


def test__InteractionComponentMetadataButton__hash():
    """
    Tests whether ``InteractionComponentMetadataButton.__hash__`` works as intended.
    """
    custom_id = 'koishi'
    
    interaction_component_metadata = InteractionComponentMetadataButton(
        custom_id = custom_id,
    )
    
    output = hash(interaction_component_metadata)
    vampytest.assert_instance(output, int)


def test__InteractionComponentMetadataButton__eq__different_type():
    """
    Tests whether ``InteractionComponentMetadataButton.__eq__`` works as intended.
    
    Case: different type.
    """
    interaction_component_metadata = InteractionComponentMetadataButton()
    
    vampytest.assert_ne(interaction_component_metadata, object())


def _iter_options__eq():
    custom_id = 'koishi'
    
    keyword_parameters = {
        'custom_id': custom_id,
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


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__InteractionComponentMetadataButton__eq__same_type(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``InteractionComponentMetadataButton.__eq__`` works as intended.
    
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
    interaction_component_metadata_0 = InteractionComponentMetadataButton(**keyword_parameters_0)
    interaction_component_metadata_1 = InteractionComponentMetadataButton(**keyword_parameters_1)
    
    output = interaction_component_metadata_0 == interaction_component_metadata_1
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__match_to_component():
    yield (
        {
            'custom_id': 'shrimp'
        },
        ComponentMetadataButton(
            custom_id = 'shrimp',
        ),
        True,
    )
    yield (
        {
            'custom_id': 'shrimp'
        },
        ComponentMetadataButton(
            custom_id = 'fry',
        ),
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__match_to_component()).returning_last())
def test__InteractionComponentMetadataButton__match_to_component(keyword_parameters, component_metadata):
    """
    Tests whether ``InteractionComponentMetadataButton._match_to_component`` works as intended.
    
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
    interaction_component_metadata = InteractionComponentMetadataButton(**keyword_parameters)
    
    output = interaction_component_metadata._match_to_component(component_metadata)
    vampytest.assert_instance(output, bool)
    return output
