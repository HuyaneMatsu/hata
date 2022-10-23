import vampytest

from ..base import ComponentMetadataBase


def _check_is_all_attribute_set(component_metadata):
    """
    Checks whether the ``ComponentMetadataBase`` has all it's attributes set.
    """
    vampytest.assert_instance(component_metadata, ComponentMetadataBase)



def test__ComponentMetadataBase__new():
    """
    Tests whether ``ComponentMetadataBase.__new__`` works as intended.
    """
    keyword_parameters = {}
    
    component_metadata = ComponentMetadataBase(keyword_parameters)
    _check_is_all_attribute_set(component_metadata)
