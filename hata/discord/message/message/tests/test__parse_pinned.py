import vampytest

from ..fields import parse_pinned


def test__parse_pinned():
    """
    Tests whether ``parse_pinned`` works as intended.
    """
    for input_data, expected_output in (
        ({}, False),
        ({'pinned': False}, False),
        ({'pinned': True}, True),
    ):
        output = parse_pinned(input_data)
        vampytest.assert_eq(output, expected_output)
