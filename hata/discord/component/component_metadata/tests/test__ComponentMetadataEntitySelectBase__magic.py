import vampytest

from ...entity_select_default_value import EntitySelectDefaultValue, EntitySelectDefaultValueType

from ..entity_select_base import ComponentMetadataEntitySelectBase


def test__ComponentMetadataEntitySelectBase__repr():
    """
    Tests whether ``ComponentMetadataEntitySelectBase.__repr__`` works as intended.
    """
    custom_id = 'oriental'
    default_values = [EntitySelectDefaultValue(EntitySelectDefaultValueType.user, 202310140004)]
    enabled = False
    max_values = 10
    min_values = 9
    placeholder = 'swing'
    
    component_metadata = ComponentMetadataEntitySelectBase(
        custom_id = custom_id,
        default_values = default_values,
        enabled = enabled,
        max_values = max_values,
        min_values = min_values,
        placeholder = placeholder,
    )
    
    vampytest.assert_instance(repr(component_metadata), str)


def test__ComponentMetadataEntitySelectBase__hash():
    """
    Tests whether ``ComponentMetadataEntitySelectBase.__hash__`` works as intended.
    """
    custom_id = 'oriental'
    default_values = [EntitySelectDefaultValue(EntitySelectDefaultValueType.user, 202310140005)]
    enabled = False
    max_values = 10
    min_values = 9
    placeholder = 'swing'
    
    component_metadata = ComponentMetadataEntitySelectBase(
        custom_id = custom_id,
        default_values = default_values,
        enabled = enabled,
        max_values = max_values,
        min_values = min_values,
        placeholder = placeholder,
    )
    
    vampytest.assert_instance(hash(component_metadata), int)


def _iter_options__eq():
    custom_id = 'oriental'
    default_values = [EntitySelectDefaultValue(EntitySelectDefaultValueType.user, 202310140006)]
    enabled = False
    max_values = 10
    min_values = 9
    placeholder = 'swing'
    required = True
    
    keyword_parameters = {
        'custom_id': custom_id,
        'default_values': default_values,
        'enabled': enabled,
        'max_values': max_values,
        'min_values': min_values,
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
            'default_values': None,
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
def test__ComponentMetadataEntitySelectBase__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``ComponentMetadataEntitySelectBase.__eq__`` works as intended.
    
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
    component_metadata_0 = ComponentMetadataEntitySelectBase(**keyword_parameters_0)
    component_metadata_1 = ComponentMetadataEntitySelectBase(**keyword_parameters_1)
    
    output = component_metadata_0 == component_metadata_1
    vampytest.assert_instance(output, bool)
    return output
