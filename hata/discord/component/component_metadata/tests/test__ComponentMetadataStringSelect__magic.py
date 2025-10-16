import vampytest

from ...string_select_option import StringSelectOption

from ..string_select import ComponentMetadataStringSelect


def test__ComponentMetadataStringSelect__repr():
    """
    Tests whether ``ComponentMetadataStringSelect.__repr__`` works as intended.
    """
    custom_id = 'oriental'
    enabled = False
    max_values = 10
    min_values = 9
    options = [StringSelectOption('yume')]
    placeholder = 'swing'
    required = True
    
    component_metadata = ComponentMetadataStringSelect(
        custom_id = custom_id,
        enabled = enabled,
        max_values = max_values,
        min_values = min_values,
        options = options,
        placeholder = placeholder,
        required = required,
    )
    
    vampytest.assert_instance(repr(component_metadata), str)


def test__ComponentMetadataStringSelect__hash():
    """
    Tests whether ``ComponentMetadataStringSelect.__hash__`` works as intended.
    """
    custom_id = 'oriental'
    enabled = False
    max_values = 10
    min_values = 9
    options = [StringSelectOption('yume')]
    placeholder = 'swing'
    required = True
    
    component_metadata = ComponentMetadataStringSelect(
        custom_id = custom_id,
        enabled = enabled,
        max_values = max_values,
        min_values = min_values,
        options = options,
        placeholder = placeholder,
        required = required,
    )
    
    vampytest.assert_instance(hash(component_metadata), int)


def _iter_options__eq():
    custom_id = 'oriental'
    enabled = False
    max_values = 10
    min_values = 9
    options = [StringSelectOption('yume')]
    placeholder = 'swing'
    required = True
    
    keyword_parameters = {
        'custom_id': custom_id,
        'enabled': enabled,
        'max_values': max_values,
        'min_values': min_values,
        'options': options,
        'placeholder': placeholder,
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
            'enabled': True,
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
            'options': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'placeholder': 'kokoro',
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
def test__ComponentMetadataStringSelect__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``ComponentMetadataStringSelect.__eq__`` works as intended.
    
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
    component_metadata_0 = ComponentMetadataStringSelect(**keyword_parameters_0)
    component_metadata_1 = ComponentMetadataStringSelect(**keyword_parameters_1)
    
    output = component_metadata_0 == component_metadata_1
    vampytest.assert_instance(output, bool)
    return output
