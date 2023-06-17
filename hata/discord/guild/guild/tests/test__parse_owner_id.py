import vampytest

from ..fields import parse_owner_id


def test__parse_owner_id():
    """
    Tests whether ``parse_owner_id`` works as intended.
    """
    owner_id = 202306100000
    
    for input_data, expected_output in (
        ({}, 0),
        ({'owner_id': None}, 0),
        ({'owner_id': str(owner_id)}, owner_id),
    ):
        output = parse_owner_id(input_data)
        vampytest.assert_eq(output, expected_output)
