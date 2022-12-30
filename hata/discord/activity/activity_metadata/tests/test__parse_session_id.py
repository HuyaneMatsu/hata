import vampytest

from ..fields import parse_session_id


def test__parse_session_id():
    """
    Tests whether ``parse_session_id`` works as intended.
    """
    for input_data, expected_output in (
        ({}, None),
        ({'session_id': None}, None),
        ({'session_id': ''}, None),
        ({'session_id': 'a'}, 'a'),
    ):
        output = parse_session_id(input_data)
        vampytest.assert_eq(output, expected_output)
