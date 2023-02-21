import vampytest

from ..fields import parse_target_id


def test__parse_target_id():
    """
    Tests whether ``parse_target_id`` works as intended.
    """
    target_id = 202302200000
    
    for input_data, expected_output in (
        ({}, 0),
        ({'id': None}, 0),
        ({'id': str(target_id)}, target_id),
    ):
        output = parse_target_id(input_data)
        vampytest.assert_eq(output, expected_output)
