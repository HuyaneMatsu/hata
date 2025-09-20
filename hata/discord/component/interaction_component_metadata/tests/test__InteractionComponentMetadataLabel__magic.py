import vampytest

from ...component import Component, ComponentType
from ...component_metadata import ComponentMetadataLabel
from ...interaction_component import InteractionComponent

from ..label import InteractionComponentMetadataLabel


def test__InteractionComponentMetadataLabel__repr():
    """
    Tests whether ``InteractionComponentMetadataLabel.__repr__`` works as intended.
    """
    interaction_component = InteractionComponent(
        ComponentType.text_input,
        custom_id = 'koishi',
    )
    
    interaction_component_metadata = InteractionComponentMetadataLabel(
        component = interaction_component
    )
    
    output = repr(interaction_component_metadata)
    vampytest.assert_instance(output, str)


def test__InteractionComponentMetadataLabel__hash():
    """
    Tests whether ``InteractionComponentMetadataLabel.__hash__`` works as intended.
    """
    interaction_component = InteractionComponent(
        ComponentType.text_input,
        custom_id = 'koishi',
    )
    
    interaction_component_metadata = InteractionComponentMetadataLabel(
        component = interaction_component,
    )
    
    output = hash(interaction_component_metadata)
    vampytest.assert_instance(output, int)


def test__InteractionComponentMetadataLabel__eq__different_type():
    """
    Tests whether ``InteractionComponentMetadataLabel.__eq__`` works as intended.
    
    Case: different type.
    """
    interaction_component_metadata = InteractionComponentMetadataLabel()
    
    vampytest.assert_ne(interaction_component_metadata, object())


def _iter_options__eq():
    interaction_component = InteractionComponent(
        ComponentType.text_input,
        custom_id = 'koishi',
    )
    
    keyword_parameters = {
        'component': interaction_component,
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
            'component': None,
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__InteractionComponentMetadataLabel__eq__same_type(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``InteractionComponentMetadataLabel.__eq__`` works as intended.
    
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
    interaction_component_metadata_0 = InteractionComponentMetadataLabel(**keyword_parameters_0)
    interaction_component_metadata_1 = InteractionComponentMetadataLabel(**keyword_parameters_1)
    
    output = interaction_component_metadata_0 == interaction_component_metadata_1
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__match_to_component():
    yield (
        {
            'component': InteractionComponent(
                ComponentType.text_input,
                custom_id = 'koishi',
            ),
        },
        ComponentMetadataLabel(
            component = Component(
                ComponentType.text_input,
                custom_id = 'koishi',
            ),
        ),
        True,
    )
    
    yield (
        {
            'component': InteractionComponent(
                ComponentType.text_input,
                custom_id = 'koishi',
            ),
        },
        ComponentMetadataLabel(
            component = None,
        ),
        False,
    )
    
    yield (
        {
            'component': InteractionComponent(
                ComponentType.text_input,
                custom_id = 'koishi',
            ),
        },
        ComponentMetadataLabel(
            component = Component(
                ComponentType.text_input,
                custom_id = 'satori',
            ),
        ),
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__match_to_component()).returning_last())
def test__InteractionComponentMetadataLabel__match_to_component(keyword_parameters, component_metadata):
    """
    Tests whether ``InteractionComponentMetadataLabel._match_to_component`` works as intended.
    
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
    interaction_component_metadata = InteractionComponentMetadataLabel(**keyword_parameters)
    
    output = interaction_component_metadata._match_to_component(component_metadata)
    vampytest.assert_instance(output, bool)
    return output
