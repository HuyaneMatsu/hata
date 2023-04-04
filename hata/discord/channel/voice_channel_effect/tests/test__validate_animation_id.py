import vampytest

from ..fields import validate_animation_id


def test__validate_animation_id__0():
    """
    Tests whether `validate_animation_id` works as intended.
    
    Case: passing.
    """
    animation_id = 202304030012
    
    for input_value, expected_output in (
        (animation_id, animation_id),
        (str(animation_id), animation_id)
    ):
        output = validate_animation_id(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_animation_id__1():
    """
    Tests whether `validate_animation_id` works as intended.
    
    Case: `ValueError`.
    """
    for input_value in (
        '1',
        -1,
    ):
        with vampytest.assert_raises(AssertionError, ValueError):
            validate_animation_id(input_value)


def test__validate_animation_id__2():
    """
    Tests whether `validate_animation_id` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_animation_id(input_value)
