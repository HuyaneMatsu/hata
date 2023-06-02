from types import FunctionType

import vampytest

from .. import get_project_structure_builder
from ..package import create_project_structure as package_project_structure_builder


def test__get_project_structure_builder__fail__unknown_layout():
    """
    Tests whether ``get_project_structure_builder`` works as intended.
    
    Case: Receives unknown layout.
    """
    with vampytest.assert_raises(RuntimeError):
        get_project_structure_builder('nue')


def test__get_project_structure_builder__fail__layout__no_builder():
    """
    Tests whether ``get_project_structure_builder`` works as intended.
    
    Case: Layout has no builder.
    """
    get_project_structure_builder_copy = FunctionType(
        get_project_structure_builder.__code__,
        {**get_project_structure_builder.__globals__, 'import_module': lambda x: object()},
        get_project_structure_builder.__name__,
        get_project_structure_builder.__defaults__,
        get_project_structure_builder.__closure__,
    )
    
    with vampytest.assert_raises(RuntimeError):
        get_project_structure_builder_copy('nue')


def test__get_project_structure_builder__pass():
    """
    Tests whether ``get_project_structure_builder`` works as intended.
    
    Case : Passing.
    """
    output = get_project_structure_builder('package')
    vampytest.assert_is(output, package_project_structure_builder)
