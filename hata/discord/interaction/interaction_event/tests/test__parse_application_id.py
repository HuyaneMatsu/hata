import vampytest

from ..fields import parse_application_id


def test__parse_application_id():
    """
    Tests whether ``parse_application_id`` works as intended.
    """
    for input_data, expected_output in (
        ({}, 0),
        ({'application_id': None}, 0),
        ({'application_id': '1'}, 1),
    ):
        output = parse_application_id(input_data)
        vampytest.assert_eq(output, expected_output)
