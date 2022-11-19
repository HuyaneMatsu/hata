import vampytest

from ..fields import parse_creator_id


def test__parse_creator_id():
    """
    Tests whether ``parse_creator_id`` works as intended.
    """
    creator_id = 202211170024
    
    for input_data, expected_output in (
        ({}, 0),
        ({'creator_id': None}, 0),
        ({'creator_id': str(creator_id)}, creator_id),
    ):
        output = parse_creator_id(input_data)
        vampytest.assert_eq(output, expected_output)
