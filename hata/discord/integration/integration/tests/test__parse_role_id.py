import vampytest

from ..fields import parse_role_id


def test__parse_role_id():
    """
    Tests whether ``parse_role_id`` works as intended.
    """
    for input_data, expected_output in (
        ({}, 0),
        ({'role_id': None}, 0),
        ({'role_id': '1'}, 1),
    ):
        output = parse_role_id(input_data)
        vampytest.assert_eq(output, expected_output)
