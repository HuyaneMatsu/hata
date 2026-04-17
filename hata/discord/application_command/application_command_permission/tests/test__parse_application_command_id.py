import vampytest

from ..fields import parse_application_command_id


def test__parse_application_command_id():
    """
    Tests whether ``parse_id`` works as intended.
    """
    application_command_id = 202302210020
    
    for input_data, expected_output in (
        ({}, 0),
        ({'id': None}, 0),
        ({'id': str(application_command_id)}, application_command_id),
    ):
        output = parse_application_command_id(input_data)
        vampytest.assert_eq(output, expected_output)
