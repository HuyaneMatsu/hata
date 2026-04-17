import vampytest

from ...radio_group_option import RadioGroupOption

from ..radio_group import ComponentMetadataRadioGroup


def test__ComponentMetadataRadioGroup__repr():
    """
    Tests whether ``ComponentMetadataRadioGroup.__repr__`` works as intended.
    """
    custom_id = 'oriental'
    options = [RadioGroupOption('yume')]
    required = True
    
    component_metadata = ComponentMetadataRadioGroup(
        custom_id = custom_id,
        options = options,
        required = required,
    )
    
    vampytest.assert_instance(repr(component_metadata), str)


def test__ComponentMetadataRadioGroup__hash():
    """
    Tests whether ``ComponentMetadataRadioGroup.__hash__`` works as intended.
    """
    custom_id = 'oriental'
    options = [RadioGroupOption('yume')]
    required = True
    
    component_metadata = ComponentMetadataRadioGroup(
        custom_id = custom_id,
        options = options,
        required = required,
    )
    
    vampytest.assert_instance(hash(component_metadata), int)


def _iter_options__eq():
    custom_id = 'oriental'
    options = [RadioGroupOption('yume')]
    required = True
    
    keyword_parameters = {
        'custom_id': custom_id,
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
def test__ComponentMetadataRadioGroup__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``ComponentMetadataRadioGroup.__eq__`` works as intended.
    
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
    component_metadata_0 = ComponentMetadataRadioGroup(**keyword_parameters_0)
    component_metadata_1 = ComponentMetadataRadioGroup(**keyword_parameters_1)
    
    output = component_metadata_0 == component_metadata_1
    vampytest.assert_instance(output, bool)
    return output
