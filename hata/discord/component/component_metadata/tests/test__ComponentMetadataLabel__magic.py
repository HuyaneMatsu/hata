import vampytest

from ...component import Component, ComponentType

from ..label import ComponentMetadataLabel


def test__ComponentMetadataLabel__repr():
    """
    Tests whether ``ComponentMetadataLabel.__repr__`` works as intended.
    """
    sub_component = Component(ComponentType.text_input, placeholder = 'chata')
    description = 'Makai route'
    label = 'Sariel'
    
    component_metadata = ComponentMetadataLabel(
        component = sub_component,
        description = description,
        label = label,
    )
    
    output = repr(component_metadata)
    vampytest.assert_instance(output, str)


def test__ComponentMetadataLabel__hash():
    """
    Tests whether ``ComponentMetadataLabel.__hash__`` works as intended.
    """
    sub_component = Component(ComponentType.text_input, placeholder = 'chata')
    description = 'Makai route'
    label = 'Sariel'
    
    component_metadata = ComponentMetadataLabel(
        component = sub_component,
        description = description,
        label = label,
    )
    
    output = hash(component_metadata)
    vampytest.assert_instance(output, int)


def test__ComponentMetadataLabel__eq__different_type():
    """
    Tests whether ``ComponentMetadataLabel.__eq__`` works as intended.
    
    Case: different type.
    """
    sub_component = Component(ComponentType.text_input, placeholder = 'chata')
    description = 'Makai route'
    label = 'Sariel'
    
    component_metadata = ComponentMetadataLabel(
        component = sub_component,
        description = description,
        label = label,
    )
    
    vampytest.assert_ne(component_metadata, object())


def _iter_options__eq():
    sub_component = Component(ComponentType.text_input, placeholder = 'chata')
    description = 'Makai route'
    label = 'Sariel'
    
    keyword_parameters = {
        'component': sub_component,
        'description': description,
        'label': label,
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
            'description': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'label': None,
        },
        False,
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
def test__ComponentMetadataLabel__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``ComponentMetadataLabel.__eq__`` works as intended.
    
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
    component_metadata_0 = ComponentMetadataLabel(**keyword_parameters_0)
    component_metadata_1 = ComponentMetadataLabel(**keyword_parameters_1)
    
    output = component_metadata_0 == component_metadata_1
    vampytest.assert_instance(output, bool)
    return output
