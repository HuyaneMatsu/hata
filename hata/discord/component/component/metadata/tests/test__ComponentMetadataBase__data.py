import vampytest

from ..base import ComponentMetadataBase

from .test__ComponentMetadataBase__constructor import _check_is_all_attribute_set


def test__ComponentMetadataBase__from_data():
    """
    Tests whether ``ComponentMetadataBase.from_data`` works as intended.
    """
    data = {}
    
    component_metadata = ComponentMetadataBase.from_data(data)
    _check_is_all_attribute_set(component_metadata)


def test__ComponentMetadataBase__to_data():
    """
    Tests whether ``ComponentMetadataBase.to_data`` works as intended.
    
    Case: include defaults.
    """
    keyword_parameters = {}
    
    component_metadata = ComponentMetadataBase(keyword_parameters)
    
    vampytest.assert_eq(
        component_metadata.to_data(
            defaults = True,
        ),
        {},
    )
