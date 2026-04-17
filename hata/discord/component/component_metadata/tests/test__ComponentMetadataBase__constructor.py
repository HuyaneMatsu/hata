import vampytest

from ..base import ComponentMetadataBase


def _assert_fields_set(component_metadata):
    """
    Checks whether the ``ComponentMetadataBase`` has all it's attributes set.
    
    Parameters
    ----------
    component_metadata : ``ComponentMetadataBase``
        Component metadata to check.
    """
    vampytest.assert_instance(component_metadata, ComponentMetadataBase)


def test__ComponentMetadataBase__new():
    """
    Tests whether ``ComponentMetadataBase.__new__`` works as intended.
    """
    component_metadata = ComponentMetadataBase()
    _assert_fields_set(component_metadata)


def test__ComponentMetadataBase__from_keyword_parameters():
    """
    Tests whether ``ComponentMetadataBase.from_keyword_parameters`` works as intended.
    """
    keyword_parameters = {}
    
    component_metadata = ComponentMetadataBase.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(component_metadata)
