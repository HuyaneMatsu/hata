import vampytest

from ..fields import parse_application_id


def test__parse_application_id():
    """
    Tests whether ``parse_id`` works as intended.
    """
    application_id = 202302210024
    
    for input_data, expected_output in (
        ({}, 0),
        ({'application_id': None}, 0),
        ({'application_id': str(application_id)}, application_id),
    ):
        output = parse_application_id(input_data)
        vampytest.assert_eq(output, expected_output)
