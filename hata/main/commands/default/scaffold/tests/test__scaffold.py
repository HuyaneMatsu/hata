from os.path import abspath as absolute_path

import vampytest

from ..command import scaffold
from ..layouts import DEFAULT_LAYOUT


scaffold = scaffold._function


@vampytest.call_with('', ('nue', 'seija'), None, None)
@vampytest.call_with('111', ('nue', 'seija'), None, None)
@vampytest.call_with('nue', ('111', 'seija'), None, None)
@vampytest.call_with('nue', ('seija', '111'), None, None)
@vampytest.call_with('nue', ('seija', 'koishi'), '111', None)
@vampytest.call_with('nue', ('seija', 'koishi'), 'kokoro', 'koakuma')
def test__scaffold__fail(name, bots, project_name, layout):
    """
    Tests whether ``scaffold`` works as intended.
    
    Case : Parameter validation fails.
    
    Parameters
    ----------
    name : `str`
        Name to create the project at.
    bots : `iterable` of `str`
        Bot names.
    project_name : `None`, `str`
        Defined project name.
    layout : `None`, `str`
        Layout value.
    """
    output = scaffold(name, *bots, project_name = project_name, layout = layout)
    
    vampytest.assert_instance(output, str)
    vampytest.assert_true(output)


@vampytest.call_with(
    'nue', ('seija', 'koishi'), 'kokoro', None, DEFAULT_LAYOUT, (absolute_path('nue'), 'kokoro', ['koishi', 'seija'])
)
@vampytest.call_with(
    'nue', ('seija', 'koishi'), None, None, DEFAULT_LAYOUT, (absolute_path('nue'), 'nue', ['koishi', 'seija'])
)
@vampytest.call_with(
    'nue', ('seija', 'koishi'), None, 'package', 'package', (absolute_path('nue'), 'nue', ['koishi', 'seija'])
)
def test__scaffold__pass(name, bots, project_name, layout, expected_layout, expected_create_project_parameters):
    """
    Tests whether ``scaffold`` works as intended.
    
    Case : Parameter validation passes, project is being created.
    
    Parameters
    ----------
    name : `str`
        Name to create the project at.
    bots : `iterable` of `str`
        Bot names.
    project_name : `None`, `str`
        Defined project name.
    layout : `None`, `str`
        Layout value.
    expected_layout : `str`
        The expected layout.
    expected_create_project_parameters : `tuple<object>`
        Expected project create parameters.
    """
    create_project_structure_called = False
    create_project_parameters = None
    import_module_called = False
    import_module_called_with = None
    
    class TestType:
        def create_project_structure(*positional_parameters):
            nonlocal create_project_structure_called
            nonlocal create_project_parameters
            
            create_project_structure_called = True
            create_project_parameters = positional_parameters
    
    
    def import_module(name):
        nonlocal TestType
        nonlocal import_module_called_with
        nonlocal import_module_called
        
        import_module_called = True
        import_module_called_with = name
        
        return TestType
    
    mocked = vampytest.mock_globals(scaffold, 2, import_module = import_module)

    output = mocked(name, *bots, project_name = project_name, layout = layout)
    
    vampytest.assert_instance(output, str)
    vampytest.assert_true(output)
    
    vampytest.assert_true(import_module_called)
    vampytest.assert_is_not(import_module_called_with, None)
    vampytest.assert_in(expected_layout, import_module_called_with)
    
    vampytest.assert_true(create_project_structure_called)
    vampytest.assert_eq(create_project_parameters, expected_create_project_parameters)
