import vampytest

from ..text import ComponentMetadataText


def test__ComponentMetadataText__repr():
    """
    Tests whether ``ComponentMetadataText.__repr__`` works as intended.
    """
    content = 'hey sister'
    
    component_metadata = ComponentMetadataText(
        content = content,
    )
    
    vampytest.assert_instance(repr(component_metadata), str)


def test__ComponentMetadataText__hash():
    """
    Tests whether ``ComponentMetadataText.__hash__`` works as intended.
    """
    content = 'hey sister'
    
    component_metadata = ComponentMetadataText(
        content = content,
    )
    
    vampytest.assert_instance(hash(component_metadata), int)


def _iter_options__eq__same_type():
    content = 'hey sister'
    
    keyword_parameters = {
        'content': content,
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
            'content': 'hey mister',
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq__same_type()).returning_last())
def test__ComponentMetadataText__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``ComponentMetadataText.__eq__`` works as intended.
    
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
    component_metadata_0 = ComponentMetadataText(**keyword_parameters_0)
    component_metadata_1 = ComponentMetadataText(**keyword_parameters_1)
    
    output = component_metadata_0 == component_metadata_1
    vampytest.assert_instance(output, bool)
    return output
