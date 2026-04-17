import vampytest

from ..preinstanced import SeparatorSpacingSize
from ..separator import ComponentMetadataSeparator


def _assert_fields_set(component_metadata):
    """
    Checks whether the given component metadata has all of its fields set.
    
    Parameters
    ----------
    component_metadata : ``ComponentMetadataSeparator``
    """
    vampytest.assert_instance(component_metadata, ComponentMetadataSeparator)
    vampytest.assert_instance(component_metadata.divider, bool)
    vampytest.assert_instance(component_metadata.spacing_size, SeparatorSpacingSize)


def test__ComponentMetadataSeparator__new__no_fields():
    """
    Tests whether ``ComponentMetadataSeparator.__new__`` works as intended.
    
    Case: No fields.
    """
    component_metadata = ComponentMetadataSeparator()
    _assert_fields_set(component_metadata)


def test__ComponentMetadataSeparator__new__all_fields():
    """
    Tests whether ``ComponentMetadataSeparator.__new__`` works as intended.
    
    Case: All fields.
    """
    divider = False
    spacing_size = SeparatorSpacingSize.large
    
    component_metadata = ComponentMetadataSeparator(
        divider = divider,
        spacing_size = spacing_size,
    )
    _assert_fields_set(component_metadata)
    vampytest.assert_eq(component_metadata.divider, divider)
    vampytest.assert_is(component_metadata.spacing_size, spacing_size)


def test__ComponentMetadataSeparator__from_keyword_parameters__no_fields():
    """
    Tests whether ``ComponentMetadataSeparator.from_keyword_parameters`` works as intended.
    
    Case: No fields.
    """
    keyword_parameters = {}
    
    component_metadata = ComponentMetadataSeparator.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(component_metadata)


def test__ComponentMetadataSeparator__from_keyword_parameters__all_fields():
    """
    Tests whether ``ComponentMetadataSeparator.from_keyword_parameters`` works as intended.
    
    Case: All fields.
    """
    divider = False
    spacing_size = SeparatorSpacingSize.large
    
    keyword_parameters = {
        'divider': divider,
        'spacing_size': spacing_size,
    }
    
    component_metadata = ComponentMetadataSeparator.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(component_metadata)
    vampytest.assert_eq(component_metadata.divider, divider)
    vampytest.assert_is(component_metadata.spacing_size, spacing_size)
