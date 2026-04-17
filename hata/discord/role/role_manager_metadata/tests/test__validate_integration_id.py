import vampytest

from ....integration import Integration

from ..fields import validate_integration_id


def test__validate_integration_id__0():
    """
    Tests whether `validate_integration_id` works as intended.
    
    Case: passing.
    """
    integration_id = 202212160002   
    
    for input_value, expected_output in (
        (None, 0),
        (integration_id, integration_id),
        (Integration.precreate(integration_id), integration_id),
        (str(integration_id), integration_id)
    ):
        output = validate_integration_id(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_integration_id__1():
    """
    Tests whether `validate_integration_id` works as intended.
    
    Case: `ValueError`.
    """
    for input_value in (
        '-1',
        -1,
    ):
        with vampytest.assert_raises(AssertionError, ValueError):
            validate_integration_id(input_value)


def test__validate_integration_id__2():
    """
    Tests whether `validate_integration_id` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_integration_id(input_value)
