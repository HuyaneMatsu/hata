import vampytest

from ..fields import parse_eula_id


def test__parse_eula_id():
    """
    Tests whether ``parse_eula_id`` works as intended.
    """
    eula_id = 202211270004
    
    for input_data, expected_output in (
        ({}, 0),
        ({'eula_id': None}, 0),
        ({'eula_id': str(eula_id)}, eula_id),
    ):
        output = parse_eula_id(input_data)
        vampytest.assert_eq(output, expected_output)
