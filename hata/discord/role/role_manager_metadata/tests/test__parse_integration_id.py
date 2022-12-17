import vampytest

from ..fields import parse_integration_id


def test__parse_integration_id():
    """
    Tests whether ``parse_integration_id`` works as intended.
    """
    integration_id = 202212160002
    
    for input_data, expected_output in (
        ({}, 0),
        ({'integration_id': None}, 0),
        ({'integration_id': str(integration_id)}, integration_id),
    ):
        output = parse_integration_id(input_data)
        vampytest.assert_eq(output, expected_output)
