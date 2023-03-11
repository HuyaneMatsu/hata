import vampytest

from ..fields import parse_id


def test__parse_id():
    """
    Tests whether ``parse_id`` works as intended.
    """
    stage_id = 202303110006
    
    for input_data, expected_output in (
        ({}, 0),
        ({'id': None}, 0),
        ({'id': str(stage_id)}, stage_id),
    ):
        output = parse_id(input_data)
        vampytest.assert_eq(output, expected_output)
