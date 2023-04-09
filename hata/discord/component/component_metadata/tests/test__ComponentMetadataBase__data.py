import vampytest

from ..base import ComponentMetadataBase

from .test__ComponentMetadataBase__constructor import _assert_fields_set


def test__ComponentMetadataBase__from_data():
    """
    Tests whether ``ComponentMetadataBase.from_data`` works as intended.
    """
    data = {}
    
    component_metadata = ComponentMetadataBase.from_data(data)
    _assert_fields_set(component_metadata)


def test__ComponentMetadataBase__to_data():
    """
    Tests whether ``ComponentMetadataBase.to_data`` works as intended.
    
    Case: include defaults.
    """
    component_metadata = ComponentMetadataBase()
    
    vampytest.assert_eq(
        component_metadata.to_data(
            defaults = True,
        ),
        {},
    )
