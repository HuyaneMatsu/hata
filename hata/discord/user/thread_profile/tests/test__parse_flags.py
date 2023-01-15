import vampytest

from ..fields import parse_flags
from ..flags import ThreadProfileFlag


def test__parse_flags():
    """
    Tests whether ``parse_flags`` works as intended.
    """
    for input_data, expected_output in (
        ({}, ThreadProfileFlag(0)),
        ({'flags': 1}, ThreadProfileFlag(1)),
    ):
        output = parse_flags(input_data)
        vampytest.assert_instance(output, ThreadProfileFlag)
        vampytest.assert_eq(output, expected_output)