import vampytest

from ..fields import parse_target_id


def test__parse_target_id():
    """
    Tests whether ``parse_target_id`` works as intended.
    """
    for input_data, expected_output in (
        ({}, 0),
        ({'target_id': None}, 0),
        ({'target_id': '1'}, 1),
    ):
        output = parse_target_id(input_data)
        vampytest.assert_eq(output, expected_output)
