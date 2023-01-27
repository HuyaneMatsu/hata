import vampytest

from ..fields import validate_old_attributes


def test__validate_old_attributes__0():
    """
    Tests whether `validate_old_attributes` works as intended.
    """
    for input_value, expected_output in (
        (None, {}),
        ({}, {}),
        ({'a': 'b'}, {'a': 'b'})
    ):
        output = validate_old_attributes(input_value)
        vampytest.assert_eq(expected_output, output)



def test__validate_old_attributes__1():
    """
    Tests whether ``validate_old_attributes`` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.5,
        {12.6: 'yukari'},
    ):
        with vampytest.assert_raises(TypeError):
            validate_old_attributes(input_value)
