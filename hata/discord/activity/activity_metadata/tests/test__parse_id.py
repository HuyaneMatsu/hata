import vampytest

from ..fields import parse_id


def test__parse_id():
    """
    Tests whether ``parse_id`` works as intended.
    """
    activity_id = 202212300001
    
    for input_data, expected_output in (
        ({}, 0),
        ({'id': None}, 0),
        ({'id': format(activity_id, 'x')}, activity_id),
    ):
        output = parse_id(input_data)
        vampytest.assert_eq(output, expected_output)
