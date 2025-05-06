import vampytest

from ....color import Color

from ...component import Component, ComponentType

from ..container import ComponentMetadataContainer


def test__ComponentMetadataContainer__repr():
    """
    Tests whether ``ComponentMetadataContainer.__repr__`` works as intended.
    """
    color = Color.from_rgb(12, 255, 26)
    components = [
        Component(ComponentType.text_display, content = 'chata'),
    ]
    spoiler = True
    
    component_metadata = ComponentMetadataContainer(
        color = color,
        components = components,
        spoiler = spoiler,
    )
    
    output = repr(component_metadata)
    vampytest.assert_instance(output, str)


def test__ComponentMetadataContainer__hash():
    """
    Tests whether ``ComponentMetadataContainer.__hash__`` works as intended.
    """
    color = Color.from_rgb(12, 255, 26)
    components = [
        Component(ComponentType.text_display, content = 'chata'),
    ]
    spoiler = True
    
    component_metadata = ComponentMetadataContainer(
        color = color,
        components = components,
        spoiler = spoiler,
    )
    
    output = hash(component_metadata)
    vampytest.assert_instance(output, int)


def _iter_options__eq__same_type():
    color = Color.from_rgb(12, 255, 26)
    components = [
        Component(ComponentType.text_display, content = 'chata'),
    ]
    spoiler = True
    
    keyword_parameters = {
        'color': color,
        'components': components,
        'spoiler': spoiler,
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
            'color': Color.from_rgb(12, 17, 26),
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'components': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'spoiler': False,
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq__same_type()).returning_last())
def test__ComponentMetadataContainer__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``ComponentMetadataContainer.__eq__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `bool`
    """
    component_metadata_0 = ComponentMetadataContainer(**keyword_parameters_0)
    component_metadata_1 = ComponentMetadataContainer(**keyword_parameters_1)
    
    output = component_metadata_0 == component_metadata_1
    vampytest.assert_instance(output, bool)
    return output
