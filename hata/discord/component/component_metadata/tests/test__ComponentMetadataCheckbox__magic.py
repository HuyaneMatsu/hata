import vampytest

from ..checkbox import ComponentMetadataCheckbox


def test__ComponentMetadataCheckbox__repr():
    """
    Tests whether ``ComponentMetadataCheckbox.__repr__`` works as intended.
    """
    custom_id = 'oriental'
    default = True
    
    component_metadata = ComponentMetadataCheckbox(
        custom_id = custom_id,
        default = default,
    )
    
    vampytest.assert_instance(repr(component_metadata), str)


def test__ComponentMetadataCheckbox__hash():
    """
    Tests whether ``ComponentMetadataCheckbox.__hash__`` works as intended.
    """
    custom_id = 'oriental'
    default = True
    
    component_metadata = ComponentMetadataCheckbox(
        custom_id = custom_id,
        default = default,
    )
    
    vampytest.assert_instance(hash(component_metadata), int)


def _iter_options__eq():
    custom_id = 'oriental'
    default = True
    
    keyword_parameters = {
        'custom_id': custom_id,
        'default': default,
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
            'custom_id': 'dystopia',
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'default': False,
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__ComponentMetadataCheckbox__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``ComponentMetadataCheckbox.__eq__`` works as intended.
    
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
    component_metadata_0 = ComponentMetadataCheckbox(**keyword_parameters_0)
    component_metadata_1 = ComponentMetadataCheckbox(**keyword_parameters_1)
    
    output = component_metadata_0 == component_metadata_1
    vampytest.assert_instance(output, bool)
    return output
