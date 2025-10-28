import vampytest

from ..attachment_input import ComponentMetadataAttachmentInput


def test__ComponentMetadataAttachmentInput__repr():
    """
    Tests whether ``ComponentMetadataAttachmentInput.__repr__`` works as intended.
    """
    custom_id = 'oriental'
    max_values = 10
    min_values = 9
    required = True
    
    component_metadata = ComponentMetadataAttachmentInput(
        custom_id = custom_id,
        max_values = max_values,
        min_values = min_values,
        required = required,
    )
    
    vampytest.assert_instance(repr(component_metadata), str)


def test__ComponentMetadataAttachmentInput__hash():
    """
    Tests whether ``ComponentMetadataAttachmentInput.__hash__`` works as intended.
    """
    custom_id = 'oriental'
    max_values = 10
    min_values = 9
    required = True
    
    component_metadata = ComponentMetadataAttachmentInput(
        custom_id = custom_id,
        max_values = max_values,
        min_values = min_values,
        required = required,
    )
    
    vampytest.assert_instance(hash(component_metadata), int)


def _iter_options__eq():
    custom_id = 'oriental'
    max_values = 10
    min_values = 9
    required = True
    
    keyword_parameters = {
        'custom_id': custom_id,
        'max_values': max_values,
        'min_values': min_values,
        'required': required,
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
            'custom_id': 'distopia',
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'max_values': 11,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'min_values': 8,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'required': False,
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__ComponentMetadataAttachmentInput__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``ComponentMetadataAttachmentInput.__eq__`` works as intended.
    
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
    component_metadata_0 = ComponentMetadataAttachmentInput(**keyword_parameters_0)
    component_metadata_1 = ComponentMetadataAttachmentInput(**keyword_parameters_1)
    
    output = component_metadata_0 == component_metadata_1
    vampytest.assert_instance(output, bool)
    return output
