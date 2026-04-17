import vampytest

from ...component import Component, ComponentType

from ..row import ComponentMetadataRow


def test__ComponentMetadataRow__repr():
    """
    Tests whether ``ComponentMetadataRow.__repr__`` works as intended.
    """
    components = [
        Component(ComponentType.button, label = 'chata'),
    ]
    
    component_metadata = ComponentMetadataRow(
        components = components,
    )
    
    output = repr(component_metadata)
    vampytest.assert_instance(output, str)


def test__ComponentMetadataRow__hash():
    """
    Tests whether ``ComponentMetadataRow.__hash__`` works as intended.
    """
    components = [
        Component(ComponentType.button, label = 'chata'),
    ]
    
    component_metadata = ComponentMetadataRow(
        components = components,
    )
    
    output = hash(component_metadata)
    vampytest.assert_instance(output, int)


def _iter_options__eq__same_type():
    components = [
        Component(ComponentType.button, label = 'chata'),
    ]
    
    keyword_parameters = {
        'components': components,
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
            'components': None,
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq__same_type()).returning_last())
def test__ComponentMetadataRow__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``ComponentMetadataRow.__eq__`` works as intended.
    
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
    component_metadata_0 = ComponentMetadataRow(**keyword_parameters_0)
    component_metadata_1 = ComponentMetadataRow(**keyword_parameters_1)
    
    output = component_metadata_0 == component_metadata_1
    vampytest.assert_instance(output, bool)
    return output
