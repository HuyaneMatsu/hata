import vampytest

from ..fields import validate_client_id


def test__validate_client_id__0():
    """
    Tests whether `validate_client_id` works as intended.
    
    Case: passing.
    """
    client_id = 202302100003
    
    for input_value, expected_output in (
        (client_id, client_id),
        (str(client_id), client_id)
    ):
        output = validate_client_id(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_client_id__1():
    """
    Tests whether `validate_client_id` works as intended.
    
    Case: `ValueError`.
    """
    for input_value in (
        '-1',
        -1,
    ):
        with vampytest.assert_raises(AssertionError, ValueError):
            validate_client_id(input_value)


def test__validate_client_id__2():
    """
    Tests whether `validate_client_id` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_client_id(input_value)
