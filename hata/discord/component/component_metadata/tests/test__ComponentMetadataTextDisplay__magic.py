import vampytest

from ..text_display import ComponentMetadataTextDisplay


def test__ComponentMetadataTextDisplay__repr():
    """
    Tests whether ``ComponentMetadataTextDisplay.__repr__`` works as intended.
    """
    content = 'hey sister'
    
    component_metadata = ComponentMetadataTextDisplay(
        content = content,
    )
    
    vampytest.assert_instance(repr(component_metadata), str)


def test__ComponentMetadataTextDisplay__hash():
    """
    Tests whether ``ComponentMetadataTextDisplay.__hash__`` works as intended.
    """
    content = 'hey sister'
    
    component_metadata = ComponentMetadataTextDisplay(
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
def test__ComponentMetadataTextDisplay__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``ComponentMetadataTextDisplay.__eq__`` works as intended.
    
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
    component_metadata_0 = ComponentMetadataTextDisplay(**keyword_parameters_0)
    component_metadata_1 = ComponentMetadataTextDisplay(**keyword_parameters_1)
    
    output = component_metadata_0 == component_metadata_1
    vampytest.assert_instance(output, bool)
    return output
