import vampytest

from ..fields import validate_hub_type
from ..preinstanced import HubType


def test__validate_hub_type__0():
    """
    Tests whether `validate_hub_type` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (HubType.college, HubType.college),
        (HubType.college.value, HubType.college)
    ):
        output = validate_hub_type(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_hub_type__1():
    """
    Tests whether `validate_hub_type` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_hub_type(input_value)
