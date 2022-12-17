import vampytest

from ..fields import parse_type
from ..preinstanced import MessageActivityType


def test__parse_type():
    """
    Tests whether ``parse_type`` works as intended.
    """
    for input_data, expected_output in (
        ({'type': MessageActivityType.join.value}, MessageActivityType.join),
    ):
        output = parse_type(input_data)
        vampytest.assert_eq(output, expected_output)
