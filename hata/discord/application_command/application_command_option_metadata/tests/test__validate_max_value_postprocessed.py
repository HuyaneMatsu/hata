import vampytest

from ..fields import validate_max_value_postprocessed


def test__validate_max_value_postprocessed__0():
    """
    Tests whether `validate_max_value_postprocessed` works as intended.
    
    Case: passing.
    """
    for input_value, input_option_type, expected_output in (
        (None, int, None),
        (None, float, None),
        (10, int, 10),
        (10.0, float, 10.0),
    ):
        output = validate_max_value_postprocessed(input_value, input_option_type)
        vampytest.assert_eq(output, expected_output)


def test__validate_max_value_postprocessed__1():
    """
    Tests whether `validate_max_value_postprocessed` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        'pepe',
    ):
        with vampytest.assert_raises(TypeError):
            validate_max_value_postprocessed(input_value, int)


def test__validate_max_value_postprocessed__2():
    """
    Tests whether `validate_max_value_postprocessed` works as intended.
    
    Case: `ValueError`.
    """
    for input_value, input_option_type in (
        (10.0, int),
        (10, float),
    ):
        with vampytest.assert_raises(ValueError):
            validate_max_value_postprocessed(input_value, input_option_type)
