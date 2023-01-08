import vampytest

from ..fields import validate_banner_id


def test__validate_banner_id__0():
    """
    Tests whether `validate_banner_id` works as intended.
    
    Case: passing.
    """
    banner_id = 202301040007
    
    for input_value, expected_output in (
        (banner_id, banner_id),
        (str(banner_id), banner_id),
    ):
        output = validate_banner_id(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_banner_id__1():
    """
    Tests whether `validate_banner_id` works as intended.
    
    Case: `ValueError`.
    """
    for input_value in (
        '1',
        -1,
    ):
        with vampytest.assert_raises(AssertionError, ValueError):
            validate_banner_id(input_value)


def test__validate_banner_id__2():
    """
    Tests whether `validate_banner_id` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_banner_id(input_value)
