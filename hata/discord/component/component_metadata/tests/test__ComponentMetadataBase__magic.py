import vampytest

from ..base import ComponentMetadataBase


def test__ComponentMetadataBase__repr():
    """
    Tests whether ``ComponentMetadataBase.__repr__`` works as intended.
    """
    component_metadata = ComponentMetadataBase()
    
    vampytest.assert_instance(repr(component_metadata), str)


def test__ComponentMetadataBase__hash():
    """
    Tests whether ``ComponentMetadataBase.__hash__`` works as intended.
    """
    component_metadata = ComponentMetadataBase()
    
    vampytest.assert_instance(hash(component_metadata), int)


def test__ComponentMetadataBase__eq__different_type():
    """
    Tests whether ``ComponentMetadataBase.__eq__`` works as intended.
    
    Case: different type.
    """
    component_metadata = ComponentMetadataBase()
    
    vampytest.assert_ne(component_metadata, object())


def _iter_options__eq():
    keyword_parameters = {}
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__ComponentMetadataBase__eq__same_type(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``ComponentMetadataBase.__eq__`` works as intended.
    
    Case: same type.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create from.
    
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance from.
    
    Returns
    -------
    output : `bool`
    """
    component_metadata_0 = ComponentMetadataBase(**keyword_parameters_0)
    component_metadata_1 = ComponentMetadataBase(**keyword_parameters_1)
    
    output = component_metadata_0 == component_metadata_1
    vampytest.assert_instance(output, bool)
    return output
