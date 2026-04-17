import vampytest

from ...component import Component, ComponentType
from ...component_metadata import ComponentMetadataRow
from ...interaction_component import InteractionComponent

from ..row import InteractionComponentMetadataRow


def test__InteractionComponentMetadataRow__repr():
    """
    Tests whether ``InteractionComponentMetadataRow.__repr__`` works as intended.
    """
    interaction_components = [
        InteractionComponent(
            ComponentType.text_input,
            custom_id = 'koishi',
        ),
        InteractionComponent(
            ComponentType.text_input,
            custom_id = 'smart',
        ),
    ]
    
    interaction_component_metadata = InteractionComponentMetadataRow(
        components = interaction_components,
    )
    
    output = repr(interaction_component_metadata)
    vampytest.assert_instance(output, str)


def test__InteractionComponentMetadataRow__hash():
    """
    Tests whether ``InteractionComponentMetadataRow.__hash__`` works as intended.
    """
    interaction_components = [
        InteractionComponent(
            ComponentType.text_input,
            custom_id = 'koishi',
        ),
        InteractionComponent(
            ComponentType.text_input,
            custom_id = 'smart',
        ),
    ]
    
    interaction_component_metadata = InteractionComponentMetadataRow(
        components = interaction_components,
    )
    
    output = hash(interaction_component_metadata)
    vampytest.assert_instance(output, int)


def test__InteractionComponentMetadataRow__eq__different_type():
    """
    Tests whether ``InteractionComponentMetadataRow.__eq__`` works as intended.
    
    Case: different type.
    """
    interaction_component_metadata = InteractionComponentMetadataRow()
    
    vampytest.assert_ne(interaction_component_metadata, object())


def _iter_options__eq():
    interaction_components = [
        InteractionComponent(
            ComponentType.text_input,
            custom_id = 'koishi',
        ),
        InteractionComponent(
            ComponentType.text_input,
            custom_id = 'smart',
        ),
    ]
    
    keyword_parameters = {
        'components': interaction_components,
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
            'components': None
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__InteractionComponentMetadataRow__eq__same_type(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``InteractionComponentMetadataRow.__eq__`` works as intended.
    
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
    interaction_component_metadata_0 = InteractionComponentMetadataRow(**keyword_parameters_0)
    interaction_component_metadata_1 = InteractionComponentMetadataRow(**keyword_parameters_1)
    
    output = interaction_component_metadata_0 == interaction_component_metadata_1
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__match_to_component():
    yield (
        {
            'components': [
                InteractionComponent(
                    ComponentType.text_input,
                    custom_id = 'koishi',
                ),
            ],
        },
        ComponentMetadataRow(
            components = [
                Component(
                    ComponentType.text_input,
                    custom_id = 'koishi',
                ),
            ],
        ),
        True,
    )
    
    yield (
        {
            'components': [
                InteractionComponent(
                    ComponentType.text_input,
                    custom_id = 'koishi',
                ),
            ],
        },
        ComponentMetadataRow(
            components = None,
        ),
        False,
    )
    
    yield (
        {
            'components': [
                InteractionComponent(
                    ComponentType.text_input,
                    custom_id = 'koishi',
                ),
            ],
        },
        ComponentMetadataRow(
            components = [
                Component(
                    ComponentType.text_input,
                    custom_id = 'satori',
                ),
            ],
        ),
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__match_to_component()).returning_last())
def test__InteractionComponentMetadataRow__match_to_component(keyword_parameters, component_metadata):
    """
    Tests whether ``InteractionComponentMetadataRow._match_to_component`` works as intended.
    
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
    interaction_component_metadata = InteractionComponentMetadataRow(**keyword_parameters)
    
    output = interaction_component_metadata._match_to_component(component_metadata)
    vampytest.assert_instance(output, bool)
    return output
