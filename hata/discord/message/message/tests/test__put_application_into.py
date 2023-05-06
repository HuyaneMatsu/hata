import vampytest

from ...message_application import MessageApplication

from ..fields import put_application_into


def test__put_application_into():
    """
    Tests whether ``put_application_into`` is working as intended.
    """
    application_id = 202304290004
    application = MessageApplication.precreate(application_id, name = 'Orin')
    
    for input_value, defaults, expected_output in (
        (None, False, {}),
        (application, False, {'application': application.to_data()}),
        (application, True, {'application': application.to_data(defaults = True)}),
    ):
        data = put_application_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
