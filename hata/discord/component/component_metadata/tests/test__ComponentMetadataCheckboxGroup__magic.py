import vampytest

from ...checkbox_group_option import CheckboxGroupOption

from ..checkbox_group import ComponentMetadataCheckboxGroup


def test__ComponentMetadataCheckboxGroup__repr():
    """
    Tests whether ``ComponentMetadataCheckboxGroup.__repr__`` works as intended.
    """
    custom_id = 'oriental'
    max_values = 10
    min_values = 9
    options = [CheckboxGroupOption('yume')]
    required = True
    
    component_metadata = ComponentMetadataCheckboxGroup(
        custom_id = custom_id,
        max_values = max_values,
        min_values = min_values,
        options = options,
        required = required,
    )
    
    vampytest.assert_instance(repr(component_metadata), str)


def test__ComponentMetadataCheckboxGroup__hash():
    """
    Tests whether ``ComponentMetadataCheckboxGroup.__hash__`` works as intended.
    """
    custom_id = 'oriental'
    max_values = 10
    min_values = 9
    options = [CheckboxGroupOption('yume')]
    required = True
    
    component_metadata = ComponentMetadataCheckboxGroup(
        custom_id = custom_id,
        max_values = max_values,
        min_values = min_values,
        options = options,
        required = required,
    )
    
    vampytest.assert_instance(hash(component_metadata), int)


def _iter_options__eq():
    custom_id = 'oriental'
    max_values = 10
    min_values = 9
    options = [CheckboxGroupOption('yume')]
    required = True
    
    keyword_parameters = {
        'custom_id': custom_id,
        'max_values': max_values,
        'min_values': min_values,
        'options': options,
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
            'custom_id': 'dystopia',
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
            'required': False,
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__ComponentMetadataCheckboxGroup__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``ComponentMetadataCheckboxGroup.__eq__`` works as intended.
    
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
    component_metadata_0 = ComponentMetadataCheckboxGroup(**keyword_parameters_0)
    component_metadata_1 = ComponentMetadataCheckboxGroup(**keyword_parameters_1)
    
    output = component_metadata_0 == component_metadata_1
    vampytest.assert_instance(output, bool)
    return output
