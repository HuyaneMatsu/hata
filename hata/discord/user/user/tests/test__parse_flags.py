import vampytest

from ..fields import parse_flags
from ..flags import UserFlag


def test__parse_flags():
    """
    Tests whether ``parse_flags`` works as intended.
    """
    for input_data, expected_output in (
        ({}, UserFlag(0)),
        ({'public_flags': 1}, UserFlag(1)),
        ({'flags': 2}, UserFlag(2)),
        ({'public_flags': 1}, UserFlag(1)),
        ({'flags': 3, 'public_flags': 1}, UserFlag(3)),
    ):
        output = parse_flags(input_data)
        vampytest.assert_instance(output, UserFlag)
        vampytest.assert_eq(output, expected_output)
