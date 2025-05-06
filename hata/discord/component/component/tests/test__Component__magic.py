import vampytest

from ..component import Component
from ..preinstanced import ComponentType


def _iter_options__iter():
    component_0 = Component(ComponentType.button, custom_id = 'chen')
    component_1 = Component(ComponentType.button, custom_id = 'satori')
    
    yield None, []
    yield [component_0], [component_0]
    yield [component_0, component_1], [component_0, component_1]


@vampytest._(vampytest.call_from(_iter_options__iter()).returning_last())
def test__Component__iter(components):
    """
    Tests whether ``Component.__iter__`` works as intended.
    
    Parameters
    ----------
    components : `None | list<str, object>`
        Components to create component with.
    
    Returns
    -------
    output : `list<Component>`
    """
    component = Component(ComponentType.row, components = components)
    return [*component]


def test__Component__repr():
    """
    Tests whether ``Component.__repr__`` works as intended.
    """
    component_type = ComponentType.button
    
    component = Component(component_type)
    
    output = repr(component)
    vampytest.assert_instance(output, str)


def test__Component__hash():
    """
    Tests whether ``Component.__hash__`` works as intended.
    """
    component_type = ComponentType.button
    custom_id = 'chen'
    
    component = Component(component_type, custom_id = custom_id)
    
    output = hash(component)
    vampytest.assert_instance(output, int)


def _iter_options__eq():
    component_type = ComponentType.button
    custom_id = 'chen'
    
    keyword_parameters = {
        'component_type': component_type,
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
            'component_type': ComponentType.user_select,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'custom_id': 'start',
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__Component__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``Component.__eq__`` works as intended.
    
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
    component_0 = Component(**keyword_parameters_0)
    component_1 = Component(**keyword_parameters_1)
    
    output = component_0 == component_1
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__len():
    content_0 = 'yukari'
    content_1 = 'chen'
    content_2 = 'ran'
    
    yield (
        {
            'component_type': ComponentType.button,
            'label': 'pop',
        },
        0,
    )
    
    yield (
        {
            'component_type': ComponentType.text_display,
            'content': content_0,
        },
        len(content_0),
    )
    
    yield (
        {
            'component_type': ComponentType.container,
            'components': [
                Component(
                    ComponentType.section,
                    components = [
                        Component(
                            ComponentType.text_display,
                            content = content_0,
                        ),
                    ],
                ),
                Component(
                    ComponentType.text_display,
                    content = content_1,
                ),
                Component(
                    ComponentType.section,
                    components = [
                        Component(
                            ComponentType.text_display,
                            content = content_2,
                        ),
                    ],
                ),
            ],
        },
        len(content_0) + len(content_1) + len(content_2),
    )


@vampytest._(vampytest.call_from(_iter_options__len()).returning_last())
def test__Component__len(keyword_parameters):
    """
    Tests whether ``Component.__len__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `int`
    """
    component = Component(**keyword_parameters)
    
    output = len(component)
    vampytest.assert_instance(output, int)
    return output
