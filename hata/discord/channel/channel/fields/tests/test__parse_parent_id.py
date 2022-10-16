import vampytest

from ..parent_id import parse_parent_id


def test__parse_parent_id():
    """
    Tests whether ``parse_parent_id`` works as intended.
    """
    for input_data, expected_output in (
        ({}, 0),
        ({'parent_id': None}, 0),
        ({'parent_id': '1'}, 1),
    ):
        output = parse_parent_id(input_data)
        vampytest.assert_eq(output, expected_output)
