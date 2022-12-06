import vampytest

from ..fields import validate_metadata_values


def test__validate_metadata_values__0():
    """
    Tests whether ``validate_metadata_values`` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (None, None),
        ({}, None),
        ({'a': 'b'}, {'a': 'b'})
    ):
        output = validate_metadata_values(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_metadata_values__1():
    """
    Tests whether ``validate_metadata_values`` works as intended.
    
    Case: `TypeError`
    """
    for input_value in (
        12.6,
        {12.6, ''},
        {'', 12.6}
    ):
        with vampytest.assert_raises(TypeError):
            validate_metadata_values(input_value)
