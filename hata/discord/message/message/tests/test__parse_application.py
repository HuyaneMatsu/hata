import vampytest

from ...message_application import MessageApplication

from ..fields import parse_application


def test__parse_application():
    """
    Tests whether ``parse_application`` works as intended.
    """
    application_id = 202304290003
    application = MessageApplication.precreate(application_id, name = 'orin')
    
    for input_data, expected_output in (
        ({}, None),
        ({'application': None}, None),
        ({'application': application.to_data()}, application),
    ):
        output = parse_application(input_data)
        vampytest.assert_eq(output, expected_output)
