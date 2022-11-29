import vampytest

from ..fields import parse_id


def test__parse_id():
    """
    Tests whether ``parse_id`` works as intended.
    """
    id_ = 202211230017
    
    for input_data, expected_output in (
        ({}, 0),
        ({'id': None}, 0),
        ({'id': str(id_)}, id_),
    ):
        output = parse_id(input_data)
        vampytest.assert_eq(output, expected_output)
