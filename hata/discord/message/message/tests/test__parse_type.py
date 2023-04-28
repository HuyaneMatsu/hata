import vampytest

from ..fields import parse_type
from ..preinstanced import MessageType


def test__parse_type():
    """
    Tests whether ``parse_type`` works as intended.
    """
    for input_data, expected_output in (
        ({}, MessageType.default),
        ({'type': MessageType.call.value}, MessageType.call),
    ):
        output = parse_type(input_data)
        vampytest.assert_eq(output, expected_output)
