import vampytest

from ..helpers import _validate_layout
from ..layouts import DEFAULT_LAYOUT


@vampytest.call_with('package', 'package')
@vampytest.call_with('', DEFAULT_LAYOUT)
@vampytest.call_with(None, DEFAULT_LAYOUT)
def test__validate_layout__passing(layout, expected_output_layout):
    """
    Tests whether ``_validate_layout`` works as intended.
    
    Case: Passing.
    
    Parameters
    ----------
    layout : `None`, `str`
        The layout value to validate.
    expected_output_layout : `str`
        The expected output to receive.
    """
    output = _validate_layout(layout)
    vampytest.assert_eq(output, (expected_output_layout, None))


@vampytest.call_with('nue')
def test__validate_layout__failing(layout):
    """
    Tests whether ``_validate_layout`` works as intended.
    
    Case: Failing.
    
    Parameters
    ----------
    layout : `None`, `str`
        The layout value to validate.
    """
    output = _validate_layout(layout)
    vampytest.assert_instance(output, tuple)
    vampytest.assert_eq(len(output), 2)
    vampytest.assert_is(output[0], None)
    vampytest.assert_instance(output[1], str)
