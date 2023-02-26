import vampytest

from ..fields import parse_allow_in_dm


def test__parse_allow_in_dm():
    """
    Tests whether ``parse_allow_in_dm`` works as intended.
    """
    for input_data, expected_output in (
        ({}, True),
        ({'dm_permission': False}, False),
        ({'dm_permission': True}, True),
    ):
        output = parse_allow_in_dm(input_data)
        vampytest.assert_eq(output, expected_output)
