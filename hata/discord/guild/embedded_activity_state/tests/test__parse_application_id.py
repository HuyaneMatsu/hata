import vampytest

from ..fields import parse_application_id


def test__parse_application_id():
    """
    Tests whether ``parse_application_id`` works as intended.
    """
    application_id = 202212250000
    
    for input_data, expected_output in (
        ({}, 0),
        ({'embedded_activity': None}, 0),
        ({'embedded_activity': {}}, 0),
        ({'embedded_activity': {'application_id': None}}, 0),
        ({'embedded_activity': {'application_id': str(application_id)}}, application_id),
    ):
        output = parse_application_id(input_data)
        vampytest.assert_eq(output, expected_output)
