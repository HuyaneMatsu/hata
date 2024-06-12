import vampytest

from ..component import Component, ComponentType
from ..component_metadata import SeparatorSpacingSize
from ..utils import create_separator


def test__create_separator():
    """
    Tests whether ``create_separator`` works as intended.
    """
    divider = False
    spacing_size = SeparatorSpacingSize.large
    
    component = create_separator(
        divider = divider,
        spacing_size = spacing_size,
    )
    
    vampytest.assert_instance(component, Component)
    vampytest.assert_is(component.type, ComponentType.separator)
    vampytest.assert_eq(component.divider, divider)
    vampytest.assert_is(component.spacing_size, spacing_size)
