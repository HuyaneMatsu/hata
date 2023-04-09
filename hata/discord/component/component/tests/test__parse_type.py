import vampytest

from ..fields import parse_type
from ..preinstanced import ComponentType


def test__parse_type():
    """
    Tests whether ``parse_type`` works as intended.
    """
    for input_data, expected_output in (
        ({}, ComponentType.none),
        ({'type': ComponentType.button.value}, ComponentType.button),
    ):
        output = parse_type(input_data)
        vampytest.assert_is(output, expected_output)
