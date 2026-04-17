from os.path import join as join_paths

import vampytest

from ..helpers import _validate_project_name


@vampytest.call_with('123', join_paths('cool', 'nue'))
@vampytest.call_with('123', 'nue')
@vampytest.call_with(None, join_paths('cool', '123'))
@vampytest.call_with(None, '123')
def test__validate_project_name__fail_project_name_invalid(input_project_name, input_name):
    """
    Tests whether ``_validate_project_name`` works as intended.
    
    Case: Failing, project name empty or not identifier.
    
    Parameters
    ----------
    input_project_name : `None`, `str`
        Project name to pass.
    input_name : `str`
        Input name to pass
    """
    output = _validate_project_name(input_project_name, input_name)
    vampytest.assert_instance(output, tuple)
    vampytest.assert_eq(len(output), 2)
    vampytest.assert_is(output[0], None)
    vampytest.assert_instance(output[1], str)


@vampytest.call_with(None, join_paths('cool', 'nue'), 'nue')
@vampytest.call_with('aya', join_paths('cool', 'nue'), 'aya')
def test__validate_project_name__pass(input_project_name, input_name, expected_output_project_name):
    """
    Tests whether ``_validate_project_name`` works as intended.
    
    Case: Passing.
    
    Parameters
    ----------
    input_project_name : `None`, `str`
        Project name to pass.
    input_name : `str`
        Input name to pass
    expected_output_project_name : `str`
        The expected outputted project name.
    """
    output = _validate_project_name(input_project_name, input_name)
    vampytest.assert_eq(output, (expected_output_project_name, None))
