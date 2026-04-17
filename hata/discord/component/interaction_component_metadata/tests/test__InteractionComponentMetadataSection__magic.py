import vampytest

from ...component import Component, ComponentType
from ...component_metadata import ComponentMetadataSection
from ...interaction_component import InteractionComponent

from ..section import InteractionComponentMetadataSection


def test__InteractionComponentMetadataSection__repr():
    """
    Tests whether ``InteractionComponentMetadataSection.__repr__`` works as intended.
    """
    interaction_components = [
        InteractionComponent(
            ComponentType.text_display,
        ),
        InteractionComponent(
            ComponentType.text_display,
        ),
    ]
    
    thumbnail = InteractionComponent(
        ComponentType.button,
        custom_id = 'alice',
    )
    
    interaction_component_metadata = InteractionComponentMetadataSection(
        components = interaction_components,
        thumbnail = thumbnail,
    )
    
    output = repr(interaction_component_metadata)
    vampytest.assert_instance(output, str)


def test__InteractionComponentMetadataSection__hash():
    """
    Tests whether ``InteractionComponentMetadataSection.__hash__`` works as intended.
    """
    interaction_components = [
        InteractionComponent(
            ComponentType.text_display,
        ),
        InteractionComponent(
            ComponentType.text_display,
        ),
    ]
    
    thumbnail = InteractionComponent(
        ComponentType.button,
        custom_id = 'alice',
    )
    
    interaction_component_metadata = InteractionComponentMetadataSection(
        components = interaction_components,
        thumbnail = thumbnail,
    )
    
    output = hash(interaction_component_metadata)
    vampytest.assert_instance(output, int)


def test__InteractionComponentMetadataSection__eq__different_type():
    """
    Tests whether ``InteractionComponentMetadataSection.__eq__`` works as intended.
    
    Case: different type.
    """
    interaction_component_metadata = InteractionComponentMetadataSection()
    
    vampytest.assert_ne(interaction_component_metadata, object())


def _iter_options__eq():
    interaction_components = [
        InteractionComponent(
            ComponentType.text_display,
        ),
        InteractionComponent(
            ComponentType.text_display,
        ),
    ]
    
    thumbnail = InteractionComponent(
        ComponentType.button,
        custom_id = 'alice',
    )
    
    keyword_parameters = {
        'components': interaction_components,
        'thumbnail': thumbnail,
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
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'thumbnail': None
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__InteractionComponentMetadataSection__eq__same_type(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``InteractionComponentMetadataSection.__eq__`` works as intended.
    
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
    interaction_component_metadata_0 = InteractionComponentMetadataSection(**keyword_parameters_0)
    interaction_component_metadata_1 = InteractionComponentMetadataSection(**keyword_parameters_1)
    
    output = interaction_component_metadata_0 == interaction_component_metadata_1
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__match_to_component():
    yield (
        {
            'components': [
                InteractionComponent(
                    ComponentType.text_display,
                ),
            ],
            'thumbnail': InteractionComponent(
                ComponentType.button,
                custom_id = 'alice',
            ),
        },
        ComponentMetadataSection(
            components = [
                Component(
                    ComponentType.text_display,
                ),
            ],
            thumbnail = Component(
                ComponentType.button,
                custom_id = 'alice',
            ),
        ),
        True,
    )
    
    yield (
        {
            'components': [
                InteractionComponent(
                    ComponentType.text_display,
                ),
            ],
        },
        ComponentMetadataSection(
            components = None,
            thumbnail = Component(
                ComponentType.button,
                custom_id = 'alice',
            ),
        ),
        False,
    )
    
    yield (
        {
            'components': [
                InteractionComponent(
                    ComponentType.text_display,
                ),
            ],
        },
        ComponentMetadataSection(
            components = [
                Component(
                    ComponentType.text_display,
                ),
            ],
            thumbnail = Component(
                ComponentType.button,
                custom_id = 'alice',
            ),
        ),
        False,
    )
    
    yield (
        {
            'components': [
                InteractionComponent(
                    ComponentType.text_display,
                ),
            ],
            'thumbnail': InteractionComponent(
                ComponentType.button,
                custom_id = 'alice',
            ),
        },
        ComponentMetadataSection(
            components = [
                Component(
                    ComponentType.text_display,
                ),
            ],
            thumbnail = None
        ),
        False,
    )
    
    yield (
        {
            'components': [
                InteractionComponent(
                    ComponentType.text_display,
                ),
            ],
            'thumbnail': InteractionComponent(
                ComponentType.button,
                custom_id = 'alice',
            ),
        },
        ComponentMetadataSection(
            components = [
                Component(
                    ComponentType.text_display,
                ),
            ],
            thumbnail = Component(
                ComponentType.button,
                custom_id = 'marisa',
            ),
        ),
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__match_to_component()).returning_last())
def test__InteractionComponentMetadataSection__match_to_component(keyword_parameters, component_metadata):
    """
    Tests whether ``InteractionComponentMetadataSection._match_to_component`` works as intended.
    
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
    interaction_component_metadata = InteractionComponentMetadataSection(**keyword_parameters)
    
    output = interaction_component_metadata._match_to_component(component_metadata)
    vampytest.assert_instance(output, bool)
    return output
