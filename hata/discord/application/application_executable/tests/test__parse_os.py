import vampytest

from ..fields import parse_os
from ..preinstanced import OperationSystem


def test__parse_os():
    """
    Tests whether `parse_os` works as intended.
    """
    for input_value, expected_output in (
        ({}, OperationSystem.none),
        ({'os': OperationSystem.linux.value}, OperationSystem.linux),
    ):
        output = parse_os(input_value)
        vampytest.assert_eq(output, expected_output)
