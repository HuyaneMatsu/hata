import vampytest

from ..preinstanced import SeparatorSpacingSize
from ..separator import ComponentMetadataSeparator

from .test__ComponentMetadataSeparator__constructor import _assert_fields_set


def test__ComponentMetadataSeparator__from_data():
    """
    Tests whether ``ComponentMetadataSeparator.from_data`` works as intended.
    """
    divider = False
    spacing_size = SeparatorSpacingSize.large
    
    data = {
        'divider': divider,
        'spacing': spacing_size.value,
    }
    
    component_metadata = ComponentMetadataSeparator.from_data(data)
    _assert_fields_set(component_metadata)
    vampytest.assert_eq(component_metadata.divider, divider)
    vampytest.assert_is(component_metadata.spacing_size, spacing_size)


def test__ComponentMetadataSeparator__to_data():
    """
    Tests whether ``ComponentMetadataSeparator.to_data`` works as intended.
    
    Case: include defaults.
    """
    divider = False
    spacing_size = SeparatorSpacingSize.large
    
    component_metadata = ComponentMetadataSeparator(
        divider = divider,
        spacing_size = spacing_size,
    )
    
    vampytest.assert_eq(
        component_metadata.to_data(
            defaults = True,
        ),
        {
            'divider': divider,
            'spacing': spacing_size.value,
        },
    )
