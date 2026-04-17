import vampytest

from ..preinstanced import SeparatorSpacingSize
from ..separator import ComponentMetadataSeparator


def test__ComponentMetadataSeparator__repr():
    """
    Tests whether ``ComponentMetadataSeparator.__repr__`` works as intended.
    """
    divider = False
    spacing_size = SeparatorSpacingSize.large
    
    component_metadata = ComponentMetadataSeparator(
        divider = divider,
        spacing_size = spacing_size,
    )
    
    vampytest.assert_instance(repr(component_metadata), str)


def test__ComponentMetadataSeparator__hash():
    """
    Tests whether ``ComponentMetadataSeparator.__hash__`` works as intended.
    """
    divider = False
    spacing_size = SeparatorSpacingSize.large
    
    component_metadata = ComponentMetadataSeparator(
        divider = divider,
        spacing_size = spacing_size,
    )
    
    vampytest.assert_instance(hash(component_metadata), int)


def _iter_options__eq__same_type():
    divider = False
    spacing_size = SeparatorSpacingSize.large
    
    keyword_parameters = {
        'divider': divider,
        'spacing_size': spacing_size,
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
            'divider': True,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'spacing_size': SeparatorSpacingSize.small,
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq__same_type()).returning_last())
def test__ComponentMetadataSeparator__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``ComponentMetadataSeparator.__eq__`` works as intended.
    
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
    component_metadata_0 = ComponentMetadataSeparator(**keyword_parameters_0)
    component_metadata_1 = ComponentMetadataSeparator(**keyword_parameters_1)
    
    output = component_metadata_0 == component_metadata_1
    vampytest.assert_instance(output, bool)
    return output
